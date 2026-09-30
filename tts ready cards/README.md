# The Awakened – Tabletop Simulator decks

Two ready-made decks for Tabletop Simulator (TTS). Every card has its **base version on
the front** and its **upgraded version on the back**, so you upgrade a card by flipping it.

| File | Contents |
|---|---|
| `Awakened Deck.json` (+ `.png` thumbnail) | All 89 cards, once each |
| `Awakened Starter Deck.json` (+ `.png`) | The starting deck: 4 Strike, 4 Defend, Hymn, Talon Rake, using the grey-background starter versions |
| `Awakened_Faces_1.jpg`, `Awakened_Backs_1.jpg` | Sheet 1: 69 cards (10 × 7) |
| `Awakened_Faces_2.jpg`, `Awakened_Backs_2.jpg` | Sheet 2: the other 20 cards (7 × 3) |
| `Awakened_Starter_Faces_1.jpg`, `Awakened_Starter_Backs_1.jpg` | Starter sheet (3 × 2) |
| `Awakened Faces 1 (10x7, 69 cards).png`, `Awakened Backs 1 (10x7, 69 cards).png` | Lossless PNG copies of sheet 1, for importing by hand |
| `Awakened Faces 2 (5x5, 24 cards).png`, `Awakened Backs 2 (5x5, 24 cards).png` | The other 20 cards plus the 4 grey-background starter versions (Strike, Defend, Hymn, Talon Rake), as PNG |

The deck files load their images straight from this GitHub repository, so no upload is
needed.

## Load a deck (quickest)

1. Copy `Awakened Deck.json` and `Awakened Deck.png` (and/or the Starter pair) into
   `Documents\My Games\Tabletop Simulator\Saves\Saved Objects\`
2. In TTS: **Objects → Saved Objects**, then click the deck to spawn it.

## Import the PNG sheets directly

Each PNG's name gives the numbers TTS asks for. In TTS: **Objects → Components → Custom →
Deck**, then for each of the two sheets:

1. **Face:** click the folder icon and pick `Awakened Faces N (...).png` (TTS uploads it to
   your Steam Cloud, or choose "Local file").
2. Tick **Unique Backs**, then **Back:** pick the matching `Awakened Backs N (...).png`.
3. **Width / Height / Number** from the file name: sheet 1 is **10 / 7 / 69**, sheet 2 is
   **5 / 5 / 24**.
4. Leave **Back is Hidden** off and **Sideways** off, then **Import**.

Do it once per sheet, then drop the two decks on top of each other to merge them. The
merged deck has all 89 cards plus the 4 starter versions (93 cards); copy the starter
Strike and Defend in TTS (Ctrl+C / Ctrl+V) to make the 4 + 4 of the starting deck.

## Or build it by hand from the web links

**Objects → Components → Custom → Deck**, then for each sheet:

| Setting | Sheet 1 | Sheet 2 | Starter |
|---|---|---|---|
| Face | raw URL of `Awakened_Faces_1.jpg` | `Awakened_Faces_2.jpg` | `Awakened_Starter_Faces_1.jpg` |
| Unique Backs | on | on | on |
| Back | `Awakened_Backs_1.jpg` | `Awakened_Backs_2.jpg` | `Awakened_Starter_Backs_1.jpg` |
| Width × Height | 10 × 7 | 7 × 3 | 3 × 2 |
| Number | 69 | 20 | 4 |
| Back is Hidden | off | off | off |

A raw URL looks like
`https://raw.githubusercontent.com/SebastianHagemeyer/sts_boardgame_awakened_one/main/tts%20ready%20cards/Awakened_Faces_1.jpg`.

## Notes

- Sheets follow TTS's limits: at most 10 × 7 cards, the bottom-right slot is the
  "hidden" card other players see for cards in someone's hand, and sheets stay under
  4096 px wide as the TTS knowledge base recommends (409 × 571 px per card).
- Regenerate after changing cards: `python render.py` then `python build/make_tts.py`.
