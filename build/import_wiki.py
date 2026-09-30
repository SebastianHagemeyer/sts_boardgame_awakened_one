"""Re-import The Awakened's cards from the Downfall wiki card list.

    python build/import_wiki.py            # writes build/awakened_wiki.json

This is how build/awakened.json was first created. awakened.json has since been
curated by hand (Void and Ceremony removed, Plume Jab removed, a few card types
changed by the balance reviews), so the import writes to a separate file for
comparison instead of overwriting it.
"""
import html as H, json, os, re, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'https://slaythespiredownfall.wiki.gg/wiki/Cards_List?character=The_Awakened'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36'}
# Awakened tokens that live in other colours on the wiki
TOKENS = {'Ceremony', 'Void', 'Plume Jab', 'Burning Study', 'Cryostasis', 'Darkleech', 'Thunderbolt', 'ESP'}


def clean(s):
    s = re.sub(r'<img[^>]*alt="(Awakened|Colorless)?Energy[^"]*"[^>]*>', '[E]', s)
    s = re.sub(r'<img[^>]*>', '', s)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('[[File:|24px|middle]] ', '')
    return re.sub(r'[ \t]+', ' ', H.unescape(s)).strip()


def main():
    page = urllib.request.urlopen(urllib.request.Request(URL, headers=UA), timeout=120).read().decode('utf-8')
    cards = []
    for box in re.split(r'(?=<div class="card-box")', page)[1:]:
        attrs = dict(re.findall(r'data-(\w+)="([^"]*)"', box[:400]))
        title = clean(re.search(r'card-title">(.*?)</div>', box, re.S).group(1))
        if attrs.get('character') != 'Awakened' and title not in TOKENS:
            continue
        if title in TOKENS and any(c['name'] == title for c in cards):
            continue
        base = re.search(r'img-base.*?alt="([^"]+)"', box, re.S).group(1)
        upg = re.search(r'img-upg.*?alt="([^"]+)"', box, re.S)
        db = clean(re.search(r'desc-base">(.*?)</div>', box, re.S).group(1))
        du = re.search(r'desc-upg"[^>]*>(.*?)</div>', box, re.S)
        cards.append(dict(name=title, token=title in TOKENS, rarity=attrs['rarity'], type=attrs['type'],
                          cost=attrs['cost'], img=base, img_up=upg.group(1) if upg else None,
                          desc=db, desc_up=clean(du.group(1)) if du else None))
    out = os.path.join(HERE, 'awakened_wiki.json')
    json.dump(cards, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f'{len(cards)} cards -> {out}')


if __name__ == '__main__':
    main()
