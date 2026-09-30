"""Render The Awakened (Downfall) cards as Slay the Spire board game cards,
using the layers exported from Template_Deck_cards.psd."""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from conversions import CARDS, BASE_COST_FIX, UPGRADED_COST, convert
from recolor import awaken

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.environ.get('TEMP', '/tmp')
LAYERS = os.path.join(HERE, 'build', 'layers')
VG = os.path.join(HERE, 'build', 'vg')
FONT = os.path.join(HERE, 'build', 'fonts', 'Kreon.ttf')
OUT = os.path.join(HERE, 'cards')
W, H = 744, 1038

CREAM = (239, 237, 211)
YELLOW = (234, 211, 26)
GREEN = (121, 172, 24)
LABEL = (78, 77, 76)
SHADOW = (20, 14, 18)

_cache = {}
def layer(name):
    if name not in _cache:
        _cache[name] = Image.open(os.path.join(LAYERS, name + '.png')).convert('RGBA')
    return _cache[name]

def font(size, weight='Regular'):
    key = ('f', size, weight)
    if key not in _cache:
        f = ImageFont.truetype(FONT, size)
        f.set_variation_by_name(weight)
        _cache[key] = f
    return _cache[key]

ICONS = {'hit': 'hit icon', 'block': 'block icon', 'str': 'strength icon', 'weak': 'weak icon',
         'vuln': 'vulnerable icon', 'aoe': 'row icon', 'E': 'energy purple icon', 'daze': 'daze icon', 'burn': 'burn icon', 'slime': 'slime icon'}

def icon(name, h):
    key = ('i', name, h)
    if key not in _cache:
        im = layer(ICONS[name])
        if name == 'E':  # Watcher pink energy -> Awakened violet
            im = awaken(im, orb_box=(0, 0, im.width, im.height))
        im = im.crop(im.getbbox())
        _cache[key] = im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
    return _cache[key]

# ---------------------------------------------------------------- frames
def unplayable_corner(fr):
    """Remove the cost orb by mirroring the (orb-less) top-right corner."""
    fr = fr.copy()
    corner = fr.crop((W - 200, 0, W, 215)).transpose(Image.FLIP_LEFT_RIGHT)
    mask = Image.new('L', (200, 215), 0)
    ImageDraw.Draw(mask).ellipse((-10, -10, 185, 195), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(6))
    fr.paste(corner, (0, 0), mask)
    return fr

def standard_banner(fr, ref):
    """The template darkens the blue (uncommon) banner on some Purple frames. Copy the standard
    print-tuned banner, ring and label pill from the matching Red frame, where both are blue."""
    import numpy as np
    from recolor import rgb2hsv
    a = np.asarray(fr).astype(float) / 255
    b = np.asarray(ref.convert('RGBA')).astype(float) / 255
    def cyan(x):
        h, s, _ = rgb2hsv(x[..., :3])
        return (h * 360 > 165) & (h * 360 < 215) & (s > 0.2) & (x[..., 3] > 0.5)
    m = cyan(a) & cyan(b)
    out = a.copy()
    out[m, :3] = b[m, :3]
    return Image.fromarray((out * 255 + 0.5).astype('uint8'), 'RGBA')

def frame(card, upgraded):
    t = card['type'] if card['type'] in ('Attack', 'Skill', 'Power') else 'Skill'
    rar = {'Basic': 'Common', 'Special': 'Uncommon'}.get(card['rarity'], card['rarity'])
    if rar not in ('Common', 'Uncommon', 'Rare'):
        rar = 'Common'
    plus = '+' if upgraded else ''
    if card['token']:
        fr = layer(f'Colorless {t}{plus} {rar if rar != "Uncommon" else "Common"}')
    else:
        key = ('frame', t, plus, rar)
        if key not in _cache:
            fr = awaken(layer(f'Purple {t}{plus} {rar}'), gem=True)
            if rar == 'Uncommon':
                fr = standard_banner(fr, layer(f'Red {t}{plus} {rar}'))
            _cache[key] = fr
        fr = _cache[key]
    if card['cost'] == 'Unplayable':
        fr = unplayable_corner(fr)
    return fr

# ---------------------------------------------------------------- art
VG_ART = (97, 150, 597, 468)        # art window in a 678px-wide VG card
BG_ART = (100, 183, 652, 558)       # area behind the template's art window

def art(card):
    im = Image.open(os.path.join(VG, card['img'].replace(' ', '_'))).convert('RGBA')
    s = 678 / im.width
    im = im.resize((678, round(im.height * s)), Image.LANCZOS)
    dy = (im.height - 874) // 2      # spell cards are a bit taller
    x0, y0, x1, y1 = VG_ART
    crop = im.crop((x0, y0 + dy, x1, y1 + dy))
    tw, th = BG_ART[2] - BG_ART[0], BG_ART[3] - BG_ART[1]
    sc = max(tw / crop.width, th / crop.height)
    crop = crop.resize((round(crop.width * sc), round(crop.height * sc)), Image.LANCZOS)
    l = (crop.width - tw) // 2
    t = (crop.height - th) // 2
    return crop.crop((l, t, l + tw, t + th))

# ---------------------------------------------------------------- text
def parse(text):
    """-> list of lines; line = list of words; word = list of (kind, value, keyword?)"""
    lines = []
    kw = False
    for raw in text.split('\n'):
        words = []
        for w in raw.split(' '):
            if not w:
                continue
            segs = []
            for part in re.split(r'(\[[a-zA-Z]+\]|\*)', w):
                if part == '*':
                    kw = not kw
                elif part.startswith('[') and part.endswith(']'):
                    segs.append(('icon', part[1:-1], kw))
                elif part:
                    segs.append(('text', part, kw))
            words.append(segs)
        lines.append(words)
    return lines

# Body text sizes measured on the rustywolf board game cards (744px wide):
#   one short line (Strike, Bash, Inflame)  -> x-height 32px, digits 46px
#   normal, 2-4 lines (Pommel Strike, Havoc)  -> x-height 27px, digits 39px
#   long text (Warcry, Fire Breathing)        -> x-height 25px
# Icons are exactly digit height with their tops level with the digits, 6px after a number.
# Lines are centred on y=737 with a pitch of 1.12 x font size.
SIZE_LARGE, SIZE_NORMAL, SIZE_LONG = 66, 56, 52
TEXT_CX, TEXT_CY, TEXT_W = 373, 737, 490
LARGE_MAX_W = 430
NUM_GAP, ICON_GAP = 3, 2
ICON_SCALE, ICON_RAISE = 1.16, -3  # icon art has soft edges: scale so the coloured part matches

def metrics(f):
    top, bottom = f.getbbox('2')[1], f.getbbox('2')[3]
    return top, bottom - top          # digit top offset from the 'la' origin, digit height

def seg_widths(word, f, ih):
    """width of each segment inc. the gap that precedes it"""
    out = []
    prev = None
    for kind, val, _ in word:
        if kind == 'text':
            w = f.getlength(val)
            gap = ICON_GAP if prev == 'icon' else 0
        else:
            w = icon(val, ih).width
            gap = NUM_GAP if (prev == 'text') else (ICON_GAP if prev == 'icon' else 0)
        out.append((gap, w))
        prev = kind
    return out

def word_width(word, f, ih):
    return sum(g + w for g, w in seg_widths(word, f, ih))

def layout(text, size, maxw):
    f = font(size)
    ih = round(metrics(f)[1] * ICON_SCALE)
    space = f.getlength(' ')
    out = []
    for words in parse(text):
        cur, cw = [], 0
        for wd in words:
            ww = word_width(wd, f, ih)
            if cur and cw + space + ww > maxw:
                out.append((cur, cw))
                cur, cw = [], 0
            cw = cw + (space if cur else 0) + ww
            cur.append(wd)
        out.append((cur, cw))
    return out, f, ih, space

def draw_runs(img, lines, f, ih, space, cx, first_top, pitch):
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fg = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ds, dg = ImageDraw.Draw(shadow), ImageDraw.Draw(fg)
    dtop, _ = metrics(f)
    for li, (words, lw) in enumerate(lines):
        digit_top = first_top + li * pitch
        y = digit_top - dtop                       # text origin ('la')
        x = cx - lw / 2
        for wi, wd in enumerate(words):
            if wi:
                x += space
            for (gap, w), (kind, val, kw) in zip(seg_widths(wd, f, ih), wd):
                x += gap
                if kind == 'text':
                    col = YELLOW if kw else CREAM
                    ds.text((x + 2, y + 3), val, font=f, fill=SHADOW + (255,))
                    dg.text((x, y), val, font=f, fill=col + (255,))
                else:
                    ic = icon(val, ih)
                    sh = Image.new('RGBA', ic.size, SHADOW + (0,))
                    sh.putalpha(ic.getchannel('A'))
                    iy = round(digit_top - ICON_RAISE - (ih - ih / ICON_SCALE) / 2)
                    shadow.alpha_composite(sh, (round(x) + 2, iy + 3))
                    fg.alpha_composite(ic, (round(x), iy))
                x += w
    shadow = shadow.filter(ImageFilter.GaussianBlur(2))
    img.alpha_composite(shadow)
    img.alpha_composite(fg)

TEXT_BOX = (122, 612, 622, 902)

CUBE_BOX = 128                 # template "--Red Box" scaled so its visible box matches Wraith Form/Devotion (~106px)
CUBE_PITCH, CUBE_TOP = 167, 794
CUBE_TEXT_TOP, CUBE_TEXT_BOTTOM = 604, 790

def cube_box():
    key = ('cube',)
    if key not in _cache:
        import numpy as np
        from recolor import rgb2hsv, hsv2rgb
        a = np.asarray(layer('--Red Box 1')).astype(float) / 255
        h, s, v = rgb2hsv(a[..., :3])
        m = s > 0.3                                    # the red fill -> Awakened slate, like the frame
        h = np.where(m, 234 / 360, h); s = np.where(m, s * 0.5, s); v = np.where(m, v * 0.62, v)
        out = np.concatenate([hsv2rgb(h, s, v), a[..., 3:]], -1)
        im = Image.fromarray((out * 255 + 0.5).astype('uint8'), 'RGBA')
        _cache[key] = im.resize((CUBE_BOX, CUBE_BOX), Image.LANCZOS)
    return _cache[key]

def draw_cubes(img, n):
    box = cube_box()
    x0 = TEXT_CX - (CUBE_PITCH * (n - 1)) / 2 - CUBE_BOX / 2
    for i in range(n):
        img.alpha_composite(box, (round(x0 + i * CUBE_PITCH), CUBE_TOP))

def body_text(img, text):
    m = re.search(r'\n?\[cubes(\d)\]', text)
    if m:
        # cube-counter cards: text sits above a row of empty cube boxes
        text = text[:m.start()] + text[m.end():]
        draw_cubes(img, int(m.group(1)))
        room = CUBE_TEXT_BOTTOM - CUBE_TEXT_TOP
        for size, lead in ((SIZE_NORMAL, 1.12), (SIZE_LONG, 1.12), (SIZE_LONG, 1.0), (48, 1.0), (44, 1.0)):
            lines, f, ih, space = layout(text, size, TEXT_W)
            pitch = round(size * lead)
            block_h = (len(lines) - 1) * pitch + metrics(f)[1]
            if block_h <= room:
                break
        first_top = (CUBE_TEXT_TOP + CUBE_TEXT_BOTTOM) / 2 - block_h / 2
        draw_runs(img, lines, f, ih, space, TEXT_CX, first_top, pitch)
        return
    plan = None
    lines, f, ih, space = layout(text, SIZE_LARGE, TEXT_W)
    if len(lines) == 1 and lines[0][1] <= LARGE_MAX_W:
        plan = (lines, f, ih, space, SIZE_LARGE)
    else:
        for size, max_lines in ((SIZE_NORMAL, 4), (SIZE_LONG, 5), (48, 6), (44, 7), (40, 8)):
            lines, f, ih, space = layout(text, size, TEXT_W)
            if len(lines) <= max_lines:
                plan = (lines, f, ih, space, size)
                break
        else:
            plan = (lines, f, ih, space, size)
    lines, f, ih, space, size = plan
    pitch = round(size * 1.12)
    block_h = (len(lines) - 1) * pitch + metrics(f)[1]
    first_top = TEXT_CY - block_h / 2
    draw_runs(img, lines, f, ih, space, TEXT_CX, first_top, pitch)

def outlined(img, xy, text, f, fill, stroke=3, anchor='mm'):
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + 2, xy[1] + 3), text, font=f, fill=SHADOW + (200,), anchor=anchor,
                            stroke_width=stroke, stroke_fill=SHADOW + (200,))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(2)))
    ImageDraw.Draw(img).text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=stroke,
                             stroke_fill=(45, 36, 40))

TRACK = 0.058   # letter spacing of card names, in em

def tracked_width(text, f, size):
    return sum(f.getlength(ch) for ch in text) + TRACK * size * (len(text) - 1)

def tracked_text(img, cx, baseline, text, f, fill, size, stroke=3):
    x = cx - tracked_width(text, f, size) / 2
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ds, d = ImageDraw.Draw(sh), ImageDraw.Draw(img)
    xs = []
    for ch in text:
        xs.append(x)
        ds.text((x + 2, baseline + 3), ch, font=f, fill=SHADOW + (200,), anchor='ls',
                stroke_width=stroke, stroke_fill=SHADOW + (200,))
        x += f.getlength(ch) + TRACK * size
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(2)))
    for x, ch in zip(xs, text):
        d.text((x, baseline), ch, font=f, fill=fill, anchor='ls', stroke_width=stroke, stroke_fill=(45, 36, 40))

RENAMED = {'Caw': 'CAW!'}   # board game name changes

def display_name(card):
    return RENAMED.get(card['name'], re.sub(r'\s*\(Awakened\)$', '', card['name']))

def type_label(card):
    if card['name'] in ('Burning Study', 'Cryostasis', 'Darkleech', 'Thunderbolt', 'ESP'):
        return 'Spell'
    return card['type']

def cost_of(card, upgraded):
    if upgraded and card['name'] in UPGRADED_COST:
        return UPGRADED_COST[card['name']]
    return BASE_COST_FIX.get(card['name'], card['cost'])

# Real starter cards (Strike, Defend, Bash...) sit on light grey instead of black
# (about 101,99,97 on the scans vs 0,0,0); shifted by the template's print tuning (0 -> 17).
STARTER_BG = (106, 104, 101)

def starter_frame(fr):
    import numpy as np
    a = np.asarray(fr).copy()
    rgb = a[..., :3].astype(int)
    m = (np.abs(rgb - 17).max(-1) <= 4) & (a[..., 3] > 0)     # the template's flat dark background
    a[m, :3] = STARTER_BG
    return Image.fromarray(a, 'RGBA')

def render(card, upgraded, starter=False):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    img.alpha_composite(art(card), BG_ART[:2])
    fr = frame(card, upgraded)
    img.alpha_composite(starter_frame(fr) if starter and not upgraded else fr)
    # cost (reference: digit fill 81-102 x 92-139 on Defend)
    cost = cost_of(card, upgraded)
    if cost != 'Unplayable':
        changed = upgraded and card['name'] in UPGRADED_COST
        outlined(img, (92, 116), cost, font(68, 'Bold'), GREEN if changed else (242, 235, 217), stroke=4)
    # name (reference: 'Defend' cap height 35px, baseline y=169, ~2.7px letter spacing)
    name = display_name(card) + ('+' if upgraded else '')
    size = 51
    while tracked_width(name, font(size), size) > 350 and size > 34:
        size -= 1
    tracked_text(img, 373, 169, name, font(size), GREEN if upgraded else CREAM, size)
    # type label (reference: Kreon Regular, neutral grey, baseline y=578)
    ImageDraw.Draw(img).text((376, 578), type_label(card), font=font(36, 'Regular'), fill=LABEL, anchor='ms')
    # body
    base, up = CARDS[card['name']][:2]
    if upgraded:
        text, _ = convert(up)
    else:
        text, _ = convert(base)
    body_text(img, text)
    return img

def slug(card):
    return re.sub(r'[^a-z0-9]+', '-', display_name(card).lower()).strip('-')

def main(only=None):
    cards = json.load(open(os.path.join(HERE, 'build', 'awakened.json')))
    os.makedirs(os.path.join(OUT, 'upgraded'), exist_ok=True)
    for c in cards:
        if only and display_name(c) not in only:
            continue
        render(c, False).save(os.path.join(OUT, slug(c) + '.png'))
        if CARDS[c['name']][1] is not None:
            render(c, True).save(os.path.join(OUT, 'upgraded', slug(c) + '.png'))
        if c['rarity'] == 'Basic':          # starter versions: grey background (upgrades keep the glow)
            os.makedirs(os.path.join(OUT, 'starter'), exist_ok=True)
            render(c, False, starter=True).save(os.path.join(OUT, 'starter', slug(c) + '.png'))
    print('done')

if __name__ == '__main__':
    main(sys.argv[1:] or None)
