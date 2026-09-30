"""Build Tabletop Simulator card sheets and a ready-to-load deck file.

    python build/make_tts.py

Writes to "tts ready cards/":
  Awakened_Faces_1.jpg / Awakened_Backs_1.jpg   10 x 7 grid, 69 cards
  Awakened_Faces_2.jpg / Awakened_Backs_2.jpg   the remaining cards
  Awakened Deck.json / .png                      all 89 cards, TTS saved object + thumbnail
  Awakened Faces/Backs N (grid, count).png       lossless PNG copies of the two main sheets, for importing by hand
  Awakened_Starter_Faces_1.jpg / _Backs_1.jpg    the grey-background starter versions
  Awakened Starter Deck.json / .png              4 Strike, 4 Defend, Hymn, Talon Rake

Faces are the base cards; each card's back (same grid position on the back
sheet) is its upgraded version, loaded with TTS's "Unique Backs" option.
TTS rules followed: at most 10 x 7 cards per sheet, the bottom-right slot is the
"hidden" image shown for cards in someone else's hand, and sheets stay at or
under 4096 px wide as the TTS knowledge base recommends.
Run render.py first so cards/ is up to date.
"""
import json, os, random, sys, urllib.parse
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import render  # noqa: E402

OUT = os.path.join(HERE, 'tts ready cards')
RAW = 'https://raw.githubusercontent.com/SebastianHagemeyer/sts_boardgame_awakened_one/main/'
CW = 409                                   # 10 x 409 = 4090 px wide sheets
CH = round(CW * render.H / render.W)       # keeps the card's 744 x 1038 shape
MAX_COLS, MAX_ROWS = 10, 7
PER_SHEET = MAX_COLS * MAX_ROWS - 1        # last slot is the hidden image
BG = (26, 22, 30)                          # fills the transparent rounded corners


def card_image(path):
    im = Image.open(path).convert('RGBA').resize((CW, CH), Image.LANCZOS)
    bg = Image.new('RGB', (CW, CH), BG)
    bg.paste(im, (0, 0), im)
    return bg


def hidden_card():
    """Generic Awakened card shown to other players for cards in a hand."""
    card = {'name': 'The Awakened', 'type': 'Power', 'rarity': 'Rare', 'token': False, 'cost': 'Unplayable',
            'img': 'Awakened-AwakenedForm.png'}
    img = Image.new('RGBA', (render.W, render.H), (0, 0, 0, 0))
    img.alpha_composite(render.art(card), render.BG_ART[:2])
    img.alpha_composite(render.frame(card, False))
    render.tracked_text(img, 373, 169, 'The Awakened', render.font(51), render.CREAM, 51)
    tmp = os.path.join(OUT, '_hidden.png')
    img.save(tmp)
    im = card_image(tmp)
    os.remove(tmp)
    return im


def grid_for(n):
    """Smallest grid (2-10 wide, 2-7 tall) that holds n cards plus the hidden slot."""
    slots = n + 1
    options = [(c * r, -c, c, r) for c in range(2, MAX_COLS + 1) for r in range(2, MAX_ROWS + 1) if c * r >= slots]
    _, _, cols, rows = min(options)
    return cols, rows


def build_sheet(entries, hidden):
    """entries: list of (card, face png, back png)"""
    cols, rows = grid_for(len(entries))
    faces = Image.new('RGB', (cols * CW, rows * CH), BG)
    backs = Image.new('RGB', (cols * CW, rows * CH), BG)
    for i, (c, face, back) in enumerate(entries):
        x, y = (i % cols) * CW, (i // cols) * CH
        faces.paste(card_image(face), (x, y))
        backs.paste(card_image(back), (x, y))
    last = (cols * rows - 1)
    for sheet in (faces, backs):
        sheet.paste(hidden, ((last % cols) * CW, (last // cols) * CH))
    return faces, backs, cols, rows


def guid():
    return '%06x' % random.randrange(16 ** 6)


def transform(y=1.0):
    return {'posX': 0.0, 'posY': y, 'posZ': 0.0, 'rotX': 0.0, 'rotY': 180.0, 'rotZ': 180.0,
            'scaleX': 1.0, 'scaleY': 1.0, 'scaleZ': 1.0}


def card_obj(c, cid, n, sheet):
    return {'GUID': guid(), 'Name': 'Card', 'Transform': transform(),
            'Nickname': render.display_name(c),
            'Description': f"{c['rarity']} {c['type']} - upgraded version on the back",
            'CardID': cid, 'CustomDeck': {str(n): sheet},
            'SidewaysCard': False, 'HideWhenFaceDown': True, 'Hands': True}


def write_deck(prefix, title, entries, counts, hidden, thumb_png, png=False):
    """entries: unique (card, face, back); counts: copies of each entry in the deck."""
    custom, contained, ids = {}, [], []
    for n, start in enumerate(range(0, len(entries), PER_SHEET), 1):
        chunk = entries[start:start + PER_SHEET]
        faces, backs, cols, rows = build_sheet(chunk, hidden)
        fname, bname = f'{prefix}_Faces_{n}.jpg', f'{prefix}_Backs_{n}.jpg'
        faces.save(os.path.join(OUT, fname), quality=92, optimize=True)
        backs.save(os.path.join(OUT, bname), quality=92, optimize=True)
        if png:
            # lossless copies for importing by hand; the name carries the numbers TTS asks for
            grid = f'{cols}x{rows}, {len(chunk)} cards'
            faces.save(os.path.join(OUT, f'{prefix} Faces {n} ({grid}).png'), optimize=True)
            backs.save(os.path.join(OUT, f'{prefix} Backs {n} ({grid}).png'), optimize=True)
        sheet = {'FaceURL': RAW + urllib.parse.quote('tts ready cards/' + fname),
                 'BackURL': RAW + urllib.parse.quote('tts ready cards/' + bname),
                 'NumWidth': cols, 'NumHeight': rows,
                 'BackIsHidden': False, 'UniqueBack': True, 'Type': 0}
        custom[str(n)] = sheet
        for i, (c, _, _) in enumerate(chunk):
            for _ in range(counts[start + i]):
                cid = n * 100 + i
                ids.append(cid)
                contained.append(card_obj(c, cid, n, sheet))
        print(f'{prefix} sheet {n}: {len(chunk)} cards, {cols} x {rows} grid, {faces.size[0]} x {faces.size[1]} px')
    deck = {'GUID': guid(), 'Name': 'Deck', 'Transform': transform(),
            'Nickname': title,
            'Description': "Fan conversion of Downfall's Awakened for Slay the Spire: The Board Game. "
                           'Base cards on the front, upgrades on the back.',
            'ColorDiffuse': {'r': 0.713, 'g': 0.713, 'b': 0.713},
            'Locked': False, 'Grid': True, 'Snap': True, 'Autoraise': True, 'Sticky': True, 'Tooltip': True,
            'HideWhenFaceDown': True, 'Hands': False, 'SidewaysCard': False,
            'DeckIDs': ids, 'CustomDeck': custom, 'ContainedObjects': contained}
    saved = {'SaveName': '', 'GameMode': '', 'Gravity': 0.5, 'PlayArea': 0.5, 'Date': '', 'Table': '', 'Sky': '',
             'Note': '', 'Rules': '', 'XmlUI': '', 'LuaScript': '', 'LuaScriptState': '',
             'ObjectStates': [deck], 'TabStates': {}, 'VersionNumber': ''}
    name = title.split(' (')[0]
    json.dump(saved, open(os.path.join(OUT, name + '.json'), 'w', encoding='utf-8'), indent=2)
    thumb = Image.open(thumb_png).convert('RGBA')
    thumb.thumbnail((256, 256), Image.LANCZOS)
    t = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    t.alpha_composite(thumb, ((256 - thumb.width) // 2, (256 - thumb.height) // 2))
    t.save(os.path.join(OUT, name + '.png'))
    print(f'{len(ids)} cards in "{name}.json"')


STARTER_DECK = [('Strike (Awakened)', 4), ('Defend (Awakened)', 4), ('Hymn', 1), ('Talon Rake', 1)]


def main():
    os.makedirs(OUT, exist_ok=True)
    cards = json.load(open(os.path.join(HERE, 'build', 'awakened.json')))
    by_name = {c['name']: c for c in cards}
    hidden = hidden_card()
    path = lambda *p: os.path.join(HERE, 'cards', *p)
    # every card once: the full card pool
    entries = [(c, path(render.slug(c) + '.png'), path('upgraded', render.slug(c) + '.png')) for c in cards]
    write_deck('Awakened', 'Awakened Deck (all 89 cards)', entries, [1] * len(entries), hidden, entries[0][1], png=True)
    # the starting deck, using the grey-background starter versions
    st = [(by_name[n], path('starter', render.slug(by_name[n]) + '.png'),
           path('upgraded', render.slug(by_name[n]) + '.png')) for n, _ in STARTER_DECK]
    write_deck('Awakened_Starter', 'Awakened Starter Deck (4 Strike, 4 Defend, Hymn, Talon Rake)', st,
               [k for _, k in STARTER_DECK], hidden, st[0][1])


if __name__ == '__main__':
    main()
