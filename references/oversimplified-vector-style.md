---
title: OverSimplified-style vector cut-out animation — reproducible art spec
created: 2026-09-25
updated: 2026-09-25
type: reference
tags: [visual, animation, craft, pattern]
sources: [quietest-room-animated-explainer]
confidence: high
---

# OverSimplified-style vector cut-out animation

Nicolas flagged the art style of the Instagram reel `Dak6Bo0s856` (the
Louisiana Purchase in 100s) as the look he wants. It was read off 51 frames
(one per 2s) through the vision chain; raw frames under
`/mnt/bulk/studio-media/artifacts/ref_dak/`. This is the spec, written so a
renderer can be built against it.

## The style in one line

Educational 2D vector cut-out animation: chibi historical caricatures moving
on an antique parchment map, bold black outlines, flat saturated territory
fills, snappy punch-in camera work.

## Characters

- Chibi, simplified caricature: **oversized rounded-pill heads, no necks,
  peg-like truncated torsos with no legs**, mitten-stub hands.
- Face: **small solid black dot eyes, thin line eyebrows, a simple slit
  mouth**. Deadpan or scheming. No rendering, no gradient, no detail.
- Identity comes from **one iconic accessory**, not from likeness: a bicorne
  hat with a cockade, a powdered rococo wig, gold-fringed epaulets, a ruffled
  cravat. Napoleon and the American diplomats are unmistakable and neither is
  drawn realistically.
- Palette for people: navy blue, charcoal black, off-white wig, warm flesh,
  brass-gold trim.

## World and backgrounds

- The environment is **one antique cartographic tabletop**: landmasses in aged
  parchment tan and sepia with faint topographical relief, oceans in
  desaturated slate-teal with nautical stippling.
- **Weathered mottled parchment grain** over land and sea, gentle **vignette
  darkening** at the frame edges.
- Physical props are placed *on* the map to localise a scene — a wooden
  presentation easel, a miniature wooden galleon. The map is a stage, not a
  picture of a place.

## Colour system

- Base: parchment tan, sepia, desaturated slate-teal.
- Territory fills are **flat, saturated, and consistent** — royal cobalt blue
  (France), bold crimson (Britain), muted teal-cyan (USA), warm ochre (Spain).
  The audience learns the colour code in the first 10 seconds and reads every
  later map without narration.
- High-contrast fills against muted sepia is the whole visual hierarchy.
- Shading is minimal: clean cell shadows on clothing folds, plus **drop
  shadows from characters onto the map plane**.

## Line and texture

- **Bold, consistent black outlines** on every asset *and* on territory
  boundaries. One weight, no variation.
- No painterly texture, no airbrush. The only texture is the paper grain.

## Diagrams and maps

- Antique continental projections under flat vector territorial fills.
- Countries are **modular physical shapes** the characters can lift, resize,
  and point at with a stick. Territory is a prop, not a backdrop.

## Motion and camera

- **Digital cut-out puppet animation** — parts move, nothing is simulated.
- Snappy 2D pans and **sudden punch-in zooms** between the wide strategic map
  and a tight character vignette.
- Slapstick beats use cartoonish **speed lines, directional chevron arrows,
  motion-blur smears, and sudden scale pops**.

## Text on screen

- Place labels (**France, Britain, USA, Spain**) and short connective phrases
  ("and offer to buy", "one city", "from the beginning", "1802"). Text is a
  caption layer over the map, never a full-screen card.

## Why this is buildable here

Every element above is vector geometry, flat fills, one outline weight, and
camera transforms — which is exactly what `remotion/` renders (React → video).
Nothing in this spec needs a video model, a stock licence, or an image
generator. Character consistency is free because the character is a component.
See [[animated-narrative-explainer]].
