"""Fetch/extract the inputs render.py needs (none of them are stored in the repo).

    python build/setup_assets.py --psd "path/to/Template_Deck_cards.psd"

1. Extracts every pixel layer of the Slay the Spire board game Photoshop template
   (Template_Deck_cards.psd, from the "StS Board game card templates for Photoshop"
   release by the Slayer Pack author) into build/layers/<layer name>.png.
2. Downloads the video game card images listed in build/awakened.json from the
   Downfall wiki into build/vg/ (the card art is cropped from these).
3. Downloads the Kreon variable font (SIL Open Font License) into build/fonts/.
"""
import argparse, json, os, sys, urllib.parse, urllib.request
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36'}
WIKI = 'https://slaythespiredownfall.wiki.gg/images/'
KREON = 'https://github.com/google/fonts/raw/main/ofl/kreon/Kreon%5Bwght%5D.ttf'


def extract_layers(psd_path):
    from psd_tools import PSDImage
    out = os.path.join(HERE, 'layers')
    os.makedirs(out, exist_ok=True)
    psd = PSDImage.open(psd_path)
    n = 0
    for layer in psd.descendants():
        if layer.kind != 'pixel':
            continue
        im = layer.topil()
        if im is None:
            continue
        name = layer.name.replace('/', '_').replace('(', '').replace(')', '')
        im.save(os.path.join(out, name + '.png'))
        n += 1
    print(f'extracted {n} layers -> {out}')


def fetch(url, path):
    if os.path.exists(path):
        return None
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        open(path, 'wb').write(data)
    except Exception as e:  # noqa: BLE001 - report and keep going
        return f'{url}: {e}'


def download_vg(limit=None):
    out = os.path.join(HERE, 'vg')
    os.makedirs(out, exist_ok=True)
    cards = json.load(open(os.path.join(HERE, 'awakened.json')))
    names = sorted({c['img'].replace(' ', '_') for c in cards})
    if limit:
        names = names[:limit]
    jobs = [(WIKI + urllib.parse.quote(n), os.path.join(out, n)) for n in names]
    with cf.ThreadPoolExecutor(8) as ex:
        errors = [e for e in ex.map(lambda j: fetch(*j), jobs) if e]
    print(f'video game images: {len(jobs) - len(errors)} ok, {len(errors)} failed')
    for e in errors:
        print('  ', e)


def download_font():
    out = os.path.join(HERE, 'fonts')
    os.makedirs(out, exist_ok=True)
    err = fetch(KREON, os.path.join(out, 'Kreon.ttf'))
    print('font:', err or 'ok')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--psd', help='path to Template_Deck_cards.psd (skip layer extraction if omitted)')
    ap.add_argument('--limit', type=int, help='only download the first N video game images (testing)')
    a = ap.parse_args()
    if a.psd:
        extract_layers(a.psd)
    elif not os.path.isdir(os.path.join(HERE, 'layers')):
        sys.exit('build/layers is missing: pass --psd "path/to/Template_Deck_cards.psd"')
    download_vg(a.limit)
    download_font()
