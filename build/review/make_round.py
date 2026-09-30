"""Build the review page for a round: python make_round.py <round> <cards json>"""
import json, sys
rnd, data = sys.argv[1], sys.argv[2]
cards = json.load(open(data, encoding='utf-8'))
t = open('template.html', encoding='utf-8').read()
subs = [
    ("    <h1>Awakened Balance Review</h1>",
     "    <h1>Awakened Balance Review</h1>\n    <div class=\"round\">Round " + rnd + "</div>"),
    ("Each card below looked too strong or too weak for the board game.",
     "Each card below looks too strong or too weak for the board game. Your changes from the last round are already on the cards."
     if rnd != '1' else "Each card below looked too strong or too weak for the board game."),
    (".tag.under { color: var(--under); }",
     ".tag.under { color: var(--under); }\n.tag.unclear { color: var(--dust); }\n.tag.fine { color: var(--ok); }\n.tag.again { color: var(--gold); }\n"
     ".round { font-family: var(--display); color: var(--dust); letter-spacing: .12em; text-transform: uppercase; font-size: .9rem; margin: -2px 0 8px; }"),
    ("text: c.verdict === 'over' ? 'Too strong' : 'Too weak' });",
     "text: c.verdict === 'over' ? 'Too strong' : c.verdict === 'under' ? 'Too weak' : c.verdict === 'fine' ? 'Looks balanced' : 'Unclear' });"),
    ("const meta = el('div', { class: 'meta' }, tag, el('span', { text: c.rarity + ' ' + c.type }));",
     "const meta = el('div', { class: 'meta' }, tag, c.again ? el('span', { class: 'tag again', text: 'Reviewed before' }) : null, el('span', { text: c.rarity + ' ' + c.type }));"),
    ("localStorage.getItem('awakened-review')", "localStorage.getItem('awakened-review-r" + rnd + "')"),
    ("localStorage.setItem('awakened-review',", "localStorage.setItem('awakened-review-r" + rnd + "',"),
    ("db.doc('reviews/' + slug)", "db.doc(COLL + '/' + slug)"),
    ("db.collection('reviews')", "db.collection(COLL)"),
    ("const CARDS = /*CARDS*/[];", "const COLL = " + json.dumps('reviews' if rnd == '1' else 'reviews-r' + rnd) + ";\nconst CARDS = " + json.dumps(cards, ensure_ascii=False) + ";"),
]
for a, b in subs:
    assert a in t, a
    t = t.replace(a, b)
open('site/index.html', 'w', encoding='utf-8').write(t)
print('built round', rnd, len(cards), 'cards')
