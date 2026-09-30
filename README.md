# The Awakened for Slay the Spire: The Board Game

A fan conversion of **The Awakened** (from the *Downfall* mod for Slay the Spire) into
cards for **Slay the Spire: The Board Game**, rendered with the community Photoshop
card template. 89 cards, each with a base and an upgraded side.

This repository holds the core code, the card data and the methods. Rendered card
images, downloaded art and the template layers are not stored here; the scripts
below rebuild them.

## Files

| Path | What it is |
|---|---|
| `conversions.py` | Every card's board game text (base and upgraded), the conversion rules (`RULES`), cost overrides, and `convert()`, which turns video game numbers into board game numbers |
| `render.py` | Renders `cards/<card>.png` and `cards/upgraded/<card>.png` from the template layers |
| `recolor.py` | Recolours the template's purple frames to the Awakened's slate-lavender |
| `build/awakened.json` | Card list: name, rarity, type, video game cost, video game image name |
| `build/setup_assets.py` | Extracts the template layers, downloads the video game card images and the Kreon font |
| `build/import_wiki.py` | Re-imports the card list from the Downfall wiki (how `awakened.json` was first made) |
| `build/review/template.html`, `build/review/make_round.py` | The balance review page used for each review round |
| `tts ready cards/` | Finished decks for Tabletop Simulator: card sheets (base on the front, upgrade on the back) and ready-to-load deck files, including a starter deck. See its README |
| `build/make_tts.py` | Builds the Tabletop Simulator sheets and deck files from `cards/` |
| `reports/STS board game card balance.md` | The balance research: board game rules numbers, enemy numbers, card price list and checklist |

## Rebuilding the cards

```bash
pip install pillow numpy scipy psd-tools
python build/setup_assets.py --psd "path/to/Photoshop card templates/Template_Deck_cards.psd"
python render.py                 # all cards
python render.py Defend "CAW!"   # or just some
python build/make_tts.py         # Tabletop Simulator sheets + deck files
```

`render.py` also writes `cards/starter/`: Strike, Defend, Hymn and Talon Rake on the light
grey background real starter cards use (their upgrades keep the normal glow).

The template is the "StS Board game card templates for Photoshop – color optimized
for professional printing" release (Template_Deck_cards.psd).

## Method

### 1. Converting numbers

Scales were measured by comparing all 282 real board game cards (transcribed from the
rustywolf compendium) with their video game originals:

| Video game | Board game |
|---|---|
| Damage 1–7 / 8–11 / 12–16 / 17–20 / 21–26 / 27–31 / 32+ | 1 / 2 / 3 / 4 / 5 / 6 / 7 |
| Block 1–6 / 7–10 / 11–15 / 16–20 / 21–26 / 27+ | 1 / 2 / 3 / 4 / 5 / 6 |
| HP loss/heal, Manaburn, Thorns | same scale as damage |
| Strength 1–4 | one [str] icon |
| Weak / Vulnerable 1–3 | one icon |
| Enemy loses Strength | [weak] icons (like Disarm, Piercing Wail) |
| "Random enemy × N" | "Each [hit] can have a different target" (like Ragnarok) |
| Energy, card draw, costs, card counts | unchanged |

In `conversions.py`, `{d6}` means "video game 6 damage" and converts through the table;
`{d16:4}` forces a value (used for one-step upgrades and balance decisions).

**Upgrades** make one change, as the real cards do: +1 to the main number, or cost −1
(the usual choice for Powers), or losing Exhaust/Ethereal, or +1 card drawn, or
"to any player".

### 2. Awakened rules decided during balancing

- **CAW!** replaces Ceremony. Each CAW! places a cube on your CAW! track; every third
  cube clears the track and gives a permanent [str]. Playing a card with CAW! counts as
  playing one Power, however many CAW!s it has. Converting cubes to [str] is not a Power.
  The track clears at the end of combat. Repeated CAW!s are written out, never numbered.
- **Void → Dazed.** The board game has no Void; every Void became the generic Dazed
  status card, worded like TURBO.
- **Manaburn** stays on an enemy until it dies. Whenever you lose energy (Drained), each
  enemy loses HP equal to its Manaburn.
- **Chant**: a bonus that works once you have played a Power. **Conjure**: add the next
  Spell from the 4-card Spellbook (Burning Study, Cryostasis, Darkleech, Thunderbolt) to
  your hand. **Awaken**: Spells use their upgraded side. **Drained**: lose [E] next turn.
- Plume Jab and the Ceremony/Void tokens were removed; no card creates them.

### 3. Balance

Cards were judged against a price list built from the real cards (full details in
`reports/`):

- A common or uncommon card gives about **cost + 1** in its main number plus one small
  extra; a rare gives about **2 × cost + 1**; starters sit 1 point under commons.
- A card draw ≈ 1 point, one-time energy ≈ 2, Weak ≈ 1, Vulnerable ≈ 2, a permanent
  [str] ≈ 2 energy, 1 HP ≈ 1 energy. Exhaust, Ethereal or a Dazed buy about +1 point.
- Anything that nets energy must Exhaust or work once per turn; "whenever" triggers need
  a once-per-turn limit or a cube counter.

The designer then reviewed the cards in rounds of about 20 on an interactive page
(`build/review/`): each card shown base and upgraded, marked Balanced or Needs work,
with the requested change applied and re-rendered before the next round.

### 4. Rendering to match the real cards

- **Frame:** the template's purple frame, recoloured (hue 234°, 55% saturation) to the
  Awakened's slate; the cost gem goes to violet (268°). The uncommon banner, ring and
  label pill are copied from the template's red frame, because the purple frames darken
  them. The template's print colour tuning is kept.
- **Art:** cropped from the video game card (678 px wide, window 97,150–597,468) and
  scaled to cover the template's art window.
- **Text**, measured on the rustywolf card scans (744 px wide):
  - one short line: 66 px Kreon; 2–4 lines: 56 px; long text: 52 px. No other sizes.
  - lines centred on y = 737 with a pitch of 1.12 × size.
  - icons are the digit height × 1.16 (their art has soft edges), tops level with the
    digits, 3 px after a number.
  - card name 51 px with 0.058 em letter spacing on a baseline at y = 169; type label
    Kreon Regular 36 px on a baseline at y = 578; cost 68 px bold at (92, 116).
- **Cube counters** (e.g. Thaumaturgy) use the template's box, recoloured and scaled to
  match Wraith Form and Devotion, in a row under the text.

## Credits and licence

- Slay the Spire © Mega Crit. Slay the Spire: The Board Game © Contention Games.
  Downfall and its card art by the Downfall team. This is an unofficial, non-commercial
  fan project.
- Card template by the author of the Slayer Pack; used under its terms (free to use and
  publish, not for sale). The template itself is not included.
- Kreon font: SIL Open Font License (downloaded by `setup_assets.py`, not included).
- The code and text in this repository are released under CC0 (see `LICENSE`).
