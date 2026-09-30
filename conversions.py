# Video game (Downfall: The Awakened) -> Slay the Spire: The Board Game conversions.
#
# The scales and upgrade style are taken from the real board game cards (rustywolf
# compendium) compared with their video game originals — see RULES below.
#
# Markup:
#   {d6}  VG damage 6 -> BG number        {b5}  VG block 5 -> BG number
#   {h6}  VG HP loss/heal -> BG number    {m8}  VG Manaburn -> BG number
#   {s2}  VG Strength -> [str] icons      {w1} Weak / {v1} Vulnerable -> icons
#   {d16:4}  VG value 16, BG value forced to 4 (one-step upgrade, see RULES)
#   [hit] [block] [str] [weak] [vuln] [aoe] [E]  -> board game icons
#   *Word*  -> yellow keyword
# Each entry: (base text, upgraded text or None, optional extra notes)

RULES = [
    ("Damage", "VG 1–7 → 1, 8–11 → 2, 12–16 → 3, 17–20 → 4, 21–26 → 5, 27–31 → 6, 32+ → 7",
     "Strike 6 → 1, Pommel Strike 9 → 2, Die Die Die 13 → 3, Carnage 20 → 4, Bludgeon 32 → 7"),
    ("Block", "VG 1–6 → 1, 7–10 → 2, 11–15 → 3, 16–20 → 4, 21–26 → 5, 27+ → 6",
     "Defend 5 → 1, Shrug It Off 8 → 2, Leg Sweep 11 → 3, Impervious 30 → 6"),
    ("HP, Manaburn, Thorns", "Same scale as damage", "Offering: lose 6 HP → lose 1 HP; Deadly Poison 5 → 1 poison"),
    ("Strength", "VG 1–4 → one [str] icon", "Inflame 2 → [str], Demon Form 2 → [str], Spot Weakness 3 → [str]"),
    ("Weak / Vulnerable", "VG 1–3 → one icon", "Bash 2 Vulnerable → [vuln], Clothesline 2 Weak → [weak]"),
    ("Enemy loses Strength", "Becomes [weak] icons", "Disarm → [weak][weak], Piercing Wail → [aoe] [weak]"),
    ("Random targets", "“Each [hit] can have a different target”", "Ragnarok, Bouncing Flask"),
    ("Energy, draw, cost, card counts", "Unchanged", "Seeing Red [E][E], Battle Trance draw 3"),
    ("Upgrades", "One improvement per card: +1 to the main number, or cost −1, or lose Exhaust / Ethereal, "
                 "or +1 card drawn, or “to any player”. Powers whose VG number grows usually get cost −1.",
     "Strike+ 2[hit]; Pommel Strike+ draws 2 (damage stays 2); Inflame+ costs 1; Flex+ loses Exhaust; Defend+ “to any player”"),
    ("Void → Dazed", "The board game has no Void; every Void becomes the generic Dazed status card", "TURBO: Put a [daze] in your discard pile."),
    ("CAW! (replaces Ceremony)", "No Ceremony cards. *CAW!* = place a cube on your CAW! track; on every 3rd cube, clear the track and gain a permanent [str]. Playing a card with *CAW!* counts as playing one Power (however many CAW!s it has); Thaumaturgy's start-of-turn CAW! counts as a Power that turn. Converting to [str] is not a Power. The track clears at the end of combat.",
     "Desperate Prayer: *CAW! CAW! CAW!* = one [str] for 1 energy, like Rupture"),
    ("Manaburn", "Manaburn stays on an enemy until it dies. When you lose energy (Drained), each enemy loses HP equal to its Manaburn.", "Designer decision, round 4"),
]

CARDS = {
# ---------------- Basic ----------------
"Defend (Awakened)": ("{b5}[block]", "{b8}[block] to any player.",
    ["Upgrade copies the board game Defend+: 2[block] to any player"]),
"Hymn": ("{b3}[block]\n*CAW!*\nNext turn, lose [E].", "{b6:2}[block]\n*CAW!*\nNext turn, lose [E].",
    ["Balance review 7: the upgrade is 2[block] with one *CAW!*", "VG Ceremony → *CAW!* (see the CAW! rule)"]),
"Strike (Awakened)": ("{d6}[hit]", "{d9}[hit]"),
"Talon Rake": ("{d6}[hit] {d6}[hit]\n*Conjure*.", "{d8}[hit] {d8}[hit]\n*Conjure*.",
    ["Upgrade like Twin Strike: 1[hit] 1[hit] → 2[hit] 2[hit]"]),
# ---------------- Common ----------------
"Brainshock": ("{d12:3}[hit]\nPut a [daze] in your discard pile.", "{d16:4}[hit]\nPut a [daze] in your discard pile.",
    ["Balance review 7: back to 3[hit] (4 upgraded), like Wild Strike"]),
"Clarion Call": ("{d8}[hit]\nIf you are *Drained* this turn, this card costs 0.", "{d11:3}[hit]\nIf you are *Drained* this turn, this card costs 0.",
    ["Balance review 5: costs 0 after a Drain instead of refunding energy"]),
"Clutch": ("{d8}[hit]\nDraw a 0-cost card.", "{d11:3}[hit]\nDraw a 0-cost card."),
"Dejection": ("{d7:2}[hit]\n*Exhaust* a card in your hand. If it was a *Spell*, *CAW!*",
              "{d10}[hit]\n*Exhaust* a card in your hand. If it was a *Spell*, *CAW! CAW!*",
    ["Balance review 2: 2[hit] base; the upgrade keeps 2[hit] and gives *CAW! CAW!*", "VG Ceremony → *CAW!* (see the CAW! rule)"]),
"Envision": ("{b4}[block]\n*Conjure*, then put the Spell on top of your draw pile.",
             "{b7}[block]\n*Conjure*, then put the Spell on top of your draw pile.",
    ["Balance review 7: the Spell goes on top of your draw pile again"]),
"Feather Flare": ("{d4}[hit]\n*Chant:* Next turn, draw 1 card.", "{d4}[hit]\n*Chant:* Next turn, draw 2 cards.",
    ["Balance review 4: the upgrade draws 2 instead of dealing 2 damage"]),
"Gather": ("{b3}[block]\n*Chant:* Put a card from your discard pile into your hand.",
           "{b6:2}[block] to any player.\n*Chant:* Put a card from your discard pile into your hand.",
    ["Balance review 3: the upgrade's Block can go to any player"]),
"Gloomguard": ("2[block]\nCosts 0 if a [daze] is in your hand.", "3[block] to any player.\nCosts 0 if a [daze] is in your hand.",
    ["Balance review 7: +1 Block"]),
"Initiation": ("{b11:2}[block]\n*CAW! CAW!*", "{b14:3}[block]\n*CAW! CAW!*",
    ["Balance review 7: 1 less Block", "VG Ceremony → *CAW!* (see the CAW! rule)"]),
"Peck": ("{b5}[block] {d1}[hit]\nDraw 1 card.", "{b5}[block] {d1}[hit]\nDraw 2 cards.",
    ["Upgrade like Pommel Strike+: only the card draw goes up (VG block 5 → 6 is below one board game step)"]),
"Planeswalk": ("Gain [E][E].\nPut [daze][daze] on top of your draw pile.\n*Exhaust*.", "Gain [E][E].\nPut a [daze] on top of your draw pile.\n*Exhaust*.",
    ["Balance review 5: [E][E] with two Dazed on top; the upgrade adds only one Dazed", "Balance review 6: Exhausts"]),
"Pluck": ("[aoe] {d2}[hit]\n*Chant:* [aoe] 1[hit]", "[aoe] {d5:2}[hit]\n*Chant:* [aoe] 1[hit]",
    ["Balance review 3: Chant: [aoe] 1[hit] instead of gaining a Plume Jab"]),
"Profane Strike": ("{d10}[hit]\nPut a card from your hand on top of your draw pile.",
                   "{d13}[hit]\nPut a card from your hand on top of your draw pile."),
"Psalm": ("[aoe] {d10}[hit] {w1}", "[aoe] {d12}[hit] {w1}",
    ["Upgrade raises only the damage (like Clothesline+); VG Weak 1 → 2 stays one icon"]),
"Recitation": ("{d6}[hit]\n*Chant:* 2[hit]", "{d8}[hit]\n*Chant:* 3[hit]",
    ["Balance review 5: the Chant hit deals 1 more"]),
"Scour": ("{d7}[hit]\n{m3:2} *Manaburn*.\nNext turn, lose [E].", "{d9}[hit]\n{m4:2} *Manaburn*.\nNext turn, lose [E].",
    ["Balance review 7: costs 0 and Drains you"]),
"Spew": ("{d6}[hit]\n[E] spent on this card counts as being *Drained*.", "{d9}[hit]\n[E] spent on this card counts as being *Drained*."),
"Unleash": ("1[hit]\n+1 damage for every *CAW!* this turn.", "2[hit]\n+1 damage for every *CAW!* this turn.",
    ["Balance review 2: scales with CAW!s this turn instead of cards in hand"]),
# ---------------- Uncommon ----------------
"Altar": ("{b5}[block]\n*Exhaust* a card in your hand.\n*Conjure*.", "{b8}[block]\n*Exhaust* a card in your hand.\n*Conjure*."),
"Blood Rite": ("{d8:3}[hit]\n*CAW!*\nNext turn, lose [E].", "{d11:3}[hit]\n*CAW! CAW!*\nNext turn, lose [E].",
    ["Balance review 5: 3[hit] with a Drain; the upgrade gives *CAW! CAW!* instead of more damage", "VG Ceremony → *CAW!* (see the CAW! rule)"]),
"Byrd's Eye": ("Choose a *Spell* to *Conjure*.", "You may refresh your *Spellbook*.\nChoose a *Spell* to *Conjure*.",
    ["Balance review 3: the upgrade's refresh is optional"]),
"Carrionmaker": ("{d9}[hit]\nRepeat for each *Spell* you played this turn. Each [hit] can have a different target.",
                 "{d12}[hit]\nRepeat for each *Spell* you played this turn. Each [hit] can have a different target."),
"Caw": ("0[hit]\n*CAW!*", "1[hit]\n*CAW!*",
    ["Renamed CAW! and redesigned (designer's call): 0[hit] means only Strength deals damage",
     "VG Chant ramp (“Caw cards deal +3 damage this combat”) replaced by *CAW!*"]),
"Chosen Verse": ("The next 2 times you play a non-Attack card this turn, draw 1 card.",
                 "The next 2 times you play a non-Attack card this turn, draw 1 card and {b4}[block].",
    ["Balance review 8: cost 1 on both; the base only draws, the upgrade also gives 1[block]"]),
"Dark Echo": ("*End of turn:*\n1 *Manaburn* to any row.", "*End of turn:*\n1 *Manaburn* to any row.",
    ["Balance review 4: Manaburn to a row instead of [aoe] 1[hit]", "Upgrade: cost 2 → 1 (same as VG)"]),
"Darkness Falls": ("Whenever you draw a [daze], 2[block].", "Whenever you draw a [daze], 2[block].",
    ["Balance review 7: 2[block] per Dazed drawn", "VG upgrade adds Innate → cost 1 → 0 (like Machine Learning+ and After Image+)"]),
"Deathcoil": ("{m8} *Manaburn*.\nNext turn, lose [E].", "{m11:3} *Manaburn*.\nNext turn, lose [E]."),
"Ensorcelate": ("{b10}[block]\nThe next Power card you play costs 0.", "{b13}[block]\nThe next Power card you play costs 0.",
    ["Balance review 4: says Power card, so a CAW! effect does not use up the discount"]),
"Eventide": ("1[hit] 1[hit] 1[hit]\nEach [hit] can have a different target.\nPut [daze][daze] on top of your draw pile.",
             "1[hit] 1[hit] 1[hit]\nEach [hit] can have a different target.\nPut a [daze] on top of your draw pile.",
    ["Balance review 8: two Dazed on top at base, one upgraded"]),
"Extension": ("{d11}[hit]\nWhenever you play a Power, return this from your discard pile to your hand.",
              "{d14}[hit]\nWhenever you play a Power, return this from your discard pile to your hand."),
"Feather Veil": ("{b10}[block]\n[daze][daze]", "{b13:2}[block]\n[daze]",
    ["Balance review: the Strength loss is replaced by two Dazed; the upgrade keeps 2[block] and adds only one Dazed"]),
"Feather Whirl": ("X[hit] 1[hit]", "X[hit] 2[hit]",
    ["Balance review 5: one X-damage hit plus a fixed second hit"]),
"Inscribe": ("Choose a *Spell*. It costs 0 this combat.", "*Conjure*.\nChoose a *Spell*. It costs 0 this combat.",
    ["Balance review 3: the chosen Spell costs 0 for the combat instead of adding 2 copies to the Spellbook"]),
"Knife's Edge": ("*CAW!*\nPut [daze][daze] in your discard pile.", "*CAW!*\nPut a [daze] in your discard pile.",
    ["Balance review: VG Strength replaced by *CAW!* (counts as playing a Power)",
     "Upgrade softens the drawback ([daze][daze] → [daze])"]),
"Midden Heap": ("{b3}[block]\nPut 1 Status or Curse from your draw or discard pile into your hand.",
                "{b3}[block]\nPut up to 2 Statuses or Curses from your draw or discard pile into your hand."),
"Mire Pit": ("[aoe] {w1}\nNext turn, lose [E].\n*Exhaust*.", "[aoe] {w1}[weak]\nNext turn, lose [E].\n*Exhaust*.",
    ["VG: ALL enemies lose 6 (8) Strength this turn → [aoe] [weak], like Piercing Wail",
     "Upgrade adds one [weak], like Disarm+ and Shockwave+"]),
"Moonlit Vision": ("The first time you play a *Spell* each turn, gain [E].", "The first time you play a *Spell* each turn, gain [E].",
    ["Upgrade: cost 2 → 1 (same as VG)"]),
"Mystic Order": ("Draw 1 card.\n*Conjure*.", "Draw 2 cards.\n*Conjure*.",
    ["Balance review 3: 1 less card drawn"]),
"Primacy": ("The first time you *CAW!* each turn, draw 1 card.", "The first 2 times you *CAW!* each turn, draw 1 card.",
    ["Balance review 2: triggers on CAW! instead of gaining [str]"]),
"Raven Strike": ("{d15}[hit]\n*Chant:* Play the top card of your draw pile for 0 Energy.",
                 "{d20}[hit]\n*Chant:* Play the top card of your draw pile for 0 Energy.",
    ["Balance review 6: says the card is played for 0 Energy"]),
"Rising Chorus": ("*Ethereal*.\nThe first *Chant* effect you play each turn activates twice.",
                  "The first *Chant* effect you play each turn activates twice.",
    ["Upgrade loses Ethereal, like Echo Form+"]),
"Singularity Shield": ("{b8:3}[block]\nNext turn, {b8:2}[block] and lose [E].", "{b10:4}[block]\nNext turn, {b10:3}[block] and lose [E].",
    ["Balance review 5: +1 on all Block", "Balance review 6: next turn's Block is 1 lower"]),
"Siphon": ("{d9}[hit]\n*Chant:* [weak]", "{d11:2}[hit]\n*Chant:* [weak][weak]",
    ["Balance review 4: the Chant applies Weak instead of stealing Strength; the upgrade adds a Weak and keeps 2[hit]"]),
"Song of Sorrow": ("*End of turn:* Deal 2 damage to any row, -1 damage for every [daze], [burn], or [slime] in your hand.",
                   "*End of turn:* Deal 3 damage to any row, -1 damage for every [daze], [burn], or [slime] in your hand.",
    ["Balance review 7: every status card in hand lowers the damage (worded like Evolve)"]),
"Soul Strike": ("{d12:3}[hit]\nCosts 1 less for each Power played this turn.", "{d18:4}[hit]\nCosts 1 less for each Power played this turn.",
    ["Balance review 7: the upgrade is 4[hit]"]),
"Spellshield": ("Whenever you *CAW!*, {b2}[block].", "Whenever you *CAW!*, {b3:2}[block].",
    ["Balance review 2: triggers on CAW! instead of Retain"]),
"Split Wide": ("{d5}[hit]\nWhenever you attack this enemy, deal 1 damage to it.\n*Exhaust*.",
               "{d7:2}[hit]\nWhenever you attack this enemy, deal 1 damage to it.\n*Exhaust*.",
    ["Balance review 2: flat 1 damage per attack instead of +1 on every [hit]"]),
"Storm Ruler": ("*Conjure*.\nYour *Thunderbolts* deal +2 damage.", "*Conjure*.\nYour *Thunderbolts* deal +2 damage.",
    ["Balance review: +2 damage instead of +1", "Upgrade: cost 1 → 0, like Accuracy+"]),
"Take Flight": ("{b12}[block]\n*Chant:* Your [block] is not removed at the start of your next turn.",
                "{b15:4}[block]\n*Chant:* Your [block] is not removed at the start of your next turn."),
"Thaumaturgy": ("*Start of turn:* *CAW!*\nPlace a cube. Then *Exhaust* if there are 2 cubes.\n[cubes2]",
                "*Retain*.\n*Start of turn:* *CAW!*\nPlace a cube. Then *Exhaust* if there are 2 cubes.\n[cubes2]",
    ["Balance review 6: Block removed: a CAW! at the start of your next 2 turns", "Upgrade gains Retain"]),
"Victuals": ("*Chant:* Gain [E].\n*Exhaust*.", "*Chant:* Gain [E][E].\n*Exhaust*.",
    ["Balance review 2: 1 less energy"]),
"Wave of Miasma": ("{b12}[block]\n[aoe] {m4} *Manaburn*.", "{b15:4}[block]\n[aoe] {m4} *Manaburn*.",
    ["Balance review 2: no longer Exhausts"]),
# ---------------- Rare ----------------
"4th Dimension": ("*Exhaust* a card in your hand. *CAW!* for each [E] it costs.\n*Exhaust*.",
                  "*Exhaust* a card in your hand. *CAW!* for each [E] it costs.\n*Exhaust*.",
    ["Balance review 3: *CAW!* per [E] of the Exhausted card instead of shuffling in 3 copies", "Upgrade: cost 1 → 0 (same as VG)"]),
"Aphotic Fount": ("*Conjure*.\nWhenever you play *Cryostasis*, it gives double the block.",
                  "*Conjure*.\nWhenever you play *Cryostasis*, it gives double the block.",
    ["Balance review: Plated Armor (not a board game mechanic) replaced by double block on Cryostasis",
     "Upgrade: cost 2 → 1 (same as VG)"]),
"Arcane Nesting": ("*Unplayable*.\nWhenever you play a Power while this is in your hand, 2[block].",
                   "*Unplayable*.\nWhenever you play a Power while this is in your hand, 3[block].",
    ["Balance review 5: 2[block] (upgraded 3) instead of healing"]),
"Archmagus": ("The first *Spell* you play each turn is played twice.", "The first *Spell* you play each turn is played twice.",
    ["Upgrade: cost 3 → 2 (same as VG)"]),
"Awakened Form": ("Whenever you play a Power, *CAW!*", "*Awaken* now.\nWhenever you play a Power, *CAW!*",
    ["Balance review 2: CAW! whenever you play a Power instead of [str]"]),
"Bloodthirst": ("{d20}[hit]\nIf this kills an enemy, draw 3 potions, choose 1, and *Exhaust* this card.",
                "{d25}[hit]\nIf this kills an enemy, draw 3 potions, choose 1, and *Exhaust* this card.",
    ["Balance review 6: draw 3 potions and choose 1 instead of a Power Potion"]),
"Demon Glyph": ("Gain [str].\nWhen you *Awaken*, gain [str].", "Gain [str].\nWhen you *Awaken*, gain [str].",
    ["VG 1 Strength and 1 Dexterity (+2 each on Awaken) → [str] now and [str] on Awaken; the Dexterity is below one board game step",
     "Upgrade: cost 1 → 0, like Inflame+ and Rupture+"]),
"Desperate Prayer": ("*CAW! CAW! CAW!*\n*Exhaust*.", "*CAW! CAW!*\n*CAW! CAW!*\n*Exhaust*.",
    ["VG 3 (4) Ceremonies → *CAW!* written once per Ceremony", "Counts as one Power played, however many *CAW!*s it has"]),
"Eclipse Embrace": ("If you have *Exhausted* [daze][daze] this turn, next turn gain [E] and draw 1 card.",
                    "If you have *Exhausted* a [daze] this turn, next turn gain [E] and draw 1 card.",
    ["Balance review 5: needs 2 Exhausted Dazed (1 upgraded); the upgrade no longer lowers the cost"]),
"Intensify": ("*Conjure*.\nThis turn, *Spells* cost 0 and you can't *Conjure* again.\n*Exhaust*.",
              "*Retain*.\n*Conjure*.\nThis turn, *Spells* cost 0 and you can't *Conjure* again.\n*Exhaust*.",
    ["Balance review 4: Exhausts"]),
"Manastorm": ("[aoe] {d14:2}[hit]\n*Conjure* twice.", "[aoe] {d18:3}[hit]\n*Conjure* twice.",
    ["Balance review 2: 1 less damage"]),
"Murder": ("{d4}[hit] {d4}[hit] {d4}[hit]\nEach [hit] can have a different target.",
           "*Retain*.\n{d4}[hit] {d4}[hit] {d4}[hit]\nEach [hit] can have a different target.",
    ["Balance review: 3 hits instead of VG's 4 (four 1[hit]s for 1 energy was far above Ragnarok)"]),
"Nihil": ("{m13:3} *Manaburn*.\n*Chant:* ALL enemies lose HP equal to their *Manaburn*.",
          "{m17:4} *Manaburn*.\n*Chant:* ALL enemies lose HP equal to their *Manaburn*.",
    ["Balance review 5: 1 less Manaburn (3, upgraded 4)"]),
"Procession": ("Draw a card. Immediately play it for 0 Energy, then shuffle a [daze] into your draw pile for each [E] it costs.\n*Exhaust*.",
               "Draw a card. Immediately play it for 0 Energy, then shuffle a [daze] into your draw pile.\n*Exhaust*.",
    ["Balance review 4: plays the card you draw (like Havoc)", "Balance review 5: the upgrade Exhausts too and adds only one Dazed"]),
"Rebirth": ("*Once per combat:* When you would die, or at the end of combat: remove all debuffs, *Awaken* and heal {h8:1} HP instead.",
            "*Once per combat:* When you would die, or at the end of combat: remove all debuffs, *Awaken* and heal {h11:2} HP instead.",
    ["Balance review: healing reduced by 1", "Balance review 4: once per combat"]),
"Skyward": ("{b18}[block]\nDraw 1 card.\nCosts 1 less for each [str] you have.", "{b24}[block]\nDraw 1 card.\nCosts 1 less for each [str] you have.",
    ["Balance review 7: cheaper per [str] instead of per Power played", "Balance review 8: cost 5 instead of 7"]),
"Sludge Bomb": ("For every [daze] in your hand, apply 1 *Manaburn*.", "For every [daze] in your hand, apply 2 *Manaburn*.",
    ["Balance review 5: 1 less Manaburn per Dazed"]),
"Spellbinder": ("*Start of turn:*\n*Conjure*.", "*Start of turn:*\n*Conjure*.", ["Upgrade: cost 1 → 0 (same as VG)"]),
"The Tower": ("[aoe] {d2}[hit]\n+1 damage for every 4 cards you created this combat.",
              "[aoe] {d3}[hit]\n+1 damage for every 3 cards you created this combat.",
    ["Balance review 3: one more created card needed per +1 damage (4, upgraded 3)"]),
# ---------------- Special ----------------
"Crusher": ("*Retain*.\n{d25:4}[hit]\nCosts 2 if you *CAW!* this turn.", "*Retain*.\n{d30:5}[hit]\nCosts 2 if you *CAW!* this turn.",
    ["Balance review 7: cost 3, or 2 after a CAW!"]),
"Daggerstorm": ("Whenever you play a *Spell*, 1[hit].", "Whenever you play a *Spell*, 2[hit].",
    ["Balance review 4: a hit, so Strength applies"]),
"Mana Shield": ("{b14:2}[block]\n*Conjure*.\nA random *Spell* in your hand costs 1 less.",
                "{b18:3}[block]\n*Conjure*.\nA random *Spell* in your hand costs 1 less.",
    ["Balance review 3: 1 less Block"]),
"Mantis": ("1[hit] 1[hit]", "1[hit] 1[hit] 1[hit]",
    ["Balance review: reworked into a Twin Strike-style Attack: Strength and Plume Jab removed", "Balance review 3: the upgrade adds a third hit instead of costing 0"]),
"Minniegun": ("{d2}[hit] {d2}[hit] {d2}[hit] {d2}[hit]\nShuffle a [daze] into your draw pile.",
              "{d2}[hit] {d2}[hit] {d2}[hit] {d2}[hit] {d2}[hit]\nShuffle a [daze] into your draw pile.",
    ["Balance review 2: one fewer hit (4, upgraded 5)"]),
"Scheme": ("The next card you play this turn that costs 2 or less costs 0.\n*Exhaust*.",
           "The next card you play this turn that costs 2 or less costs 0.\n*Exhaust*.",
    ["Balance review 7: Exhausts", "Upgrade: cost 1 → 0, like Double Tap+"]),
"Sign in Blood": ("Lose {h2} HP.\nDraw 3 cards.\n*Exhaust*.", "Lose {h2} HP.\nDraw 4 cards.\n*Exhaust*.",
    ["Balance review: Strength gain removed"]),
"Spreading Spores": ("*Ethereal*.\n*Start of turn:*\n1 *Manaburn* to any enemy.", "*Ethereal*.\n*Start of turn:*\n2 *Manaburn* to any enemy.",
    ["Balance review 2: Thorns and the self-copy removed; applies Manaburn at the start of each turn", "Balance review 8: 1 less Manaburn"]),
"The Encyclopedia": ("The next 2 cards you play this turn cost 2 less.\n*Exhaust*.", "The next 3 cards you play this turn cost 2 less.\n*Exhaust*.",
    ["Balance review 4: reworked: no random cards, the next cards cost less"]),
# ---------------- Spells ----------------
"Burning Study": ("*Retain*.\n[aoe] {w1}\n*Exhaust*.", "*Retain*.\n[aoe] {w2}[weak]\n*Exhaust*.",
    ["Balance review 2: Strength gain removed", "Spells use their upgraded side after you *Awaken*"]),
"Cryostasis": ("*Retain*.\n{b10}[block] to any player.\n*Exhaust*.", "*Retain*.\n{b13}[block] to any player.\n*Exhaust*.",
    ["Balance review 3: Block can go to any player", "Spells use their upgraded side after you *Awaken*"]),
"Darkleech": ("*Retain*.\n{v1}\n{m4} *Manaburn*.\n*Exhaust*.", "*Retain*.\n{v2}\n{m6:2} *Manaburn*.\n*Exhaust*.",
    ["Spells use their upgraded side after you *Awaken*"]),
"Thunderbolt": ("*Retain*.\n{d12}[hit]\n*Exhaust*.", "*Retain*.\n{d18}[hit]\n*Exhaust*.",
    ["Spells use their upgraded side after you *Awaken*"]),
"ESP": ("*Retain*.\nDraw 1 card.\n*Exhaust*.", "*Retain*.\nDraw 2 cards.\n*Exhaust*.",
    ["Spells use their upgraded side after you *Awaken*"]),
}

# Wiki data fixes, and upgraded costs (VG cost changes plus board-game-style cost upgrades)
BASE_COST_FIX = {"Aphotic Fount": "2", "Demon Glyph": "2", "Spellbinder": "2", "Crusher": "3", "Scour": "0", "Skyward": "5"}
UPGRADED_COST = {"Dark Echo": "1", "Moonlit Vision": "1", "4th Dimension": "0", "Aphotic Fount": "1",
                 "Archmagus": "2", "Spellbinder": "1",
                 "Darkness Falls": "0", "Storm Ruler": "0", "Demon Glyph": "1", "Scheme": "0"}

KIND = {'d': 'damage', 'b': 'Block', 'h': 'HP', 'm': 'Manaburn', 't': 'Thorns',
        's': 'Strength', 'w': 'Weak', 'v': 'Vulnerable'}
ICON = {'d': '[hit]', 'b': '[block]', 's': '[str]', 'w': '[weak]', 'v': '[vuln]'}
NUMBER_KINDS = 'dbhmt'   # printed as a number; s/w/v are printed as repeated icons

DMG = [(7, 1), (11, 2), (16, 3), (20, 4), (26, 5), (31, 6), (35, 7)]
BLK = [(6, 1), (10, 2), (15, 3), (20, 4), (26, 5), (31, 6)]

def conv(kind, vg):
    if kind in 'dhmt':
        return next((bg for top, bg in DMG if vg <= top), round(vg / 4.6))
    if kind == 'b':
        return next((bg for top, bg in BLK if vg <= top), round(vg / 5))
    if kind == 's':
        return 1 if vg <= 4 else 2
    if kind in 'wv':
        return 1 if vg <= 3 else 2
    raise ValueError(kind)

import re
TOK = re.compile(r'\{([dbhmtswv])(\d+)(?::(\d+))?\}')

def convert(text):
    """Return (board game text, conversion notes)."""
    notes = []
    def rep(m):
        k, v = m.group(1), int(m.group(2))
        out = int(m.group(3)) if m.group(3) else conv(k, v)
        if k in NUMBER_KINDS:
            shown = f"{out}{ICON.get(k, ' ' + KIND[k])}"
            res = str(out)
        else:
            shown = ICON[k] * out
            res = shown
        note = f"VG {v} {KIND[k]} → {shown}"
        if m.group(3):
            note += " (one-step upgrade)"
        if note not in notes:
            notes.append(note)
        return res
    return TOK.sub(rep, text), notes

def entry(name):
    e = CARDS[name]
    return e[0], e[1], (e[2] if len(e) > 2 else [])
