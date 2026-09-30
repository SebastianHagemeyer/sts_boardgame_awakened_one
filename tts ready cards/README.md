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

The deck files load their images straight from this GitHub repository, so no upload is
needed.

## Load a deck (quickest)

1. Copy `Awakened Deck.json` and `Awakened Deck.png` (and/or the Starter pair) into
   `Documents\My Games\Tabletop Simulator\Saves\Saved Objects\`
2. In TTS: **Objects → Saved Objects**, then click the deck to spawn it.

## Or build it by hand in TTS

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
