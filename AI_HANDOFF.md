# AI Handoff: Secret Manifestation Cards Game

## Current State

This folder currently contains a local card database and a styled viewer for "The Secret Manifestation Cards".

Files of interest:

- `secret_oracle_v6.html`: Latest version with Traditional Chinese UI, improved aesthetics, and question input.
- `cards_viewer.html`: Original database viewer UI.
- `database/cards.json`: card data with titles, text, border colors, and source image references
- `database/cards.csv`: CSV export of the same data
- `database/cards.sqlite`: SQLite copy of the card database
- `assets/original-card-background.png`: generated original card background asset
- `source_images/`: reference photos used while cataloging cards

## What The User Wants Next

Build this into a game-like app for mobile and web.

The core idea:

- user asks a question
- app randomly draws one card
- app reveals the card
- app explains the meaning / prompt for that card
- mobile experience should be first-class, with a web interface too

The vibe should feel like a devotional / oracle-style card draw app, not a plain database.

## Important UI Notes From The User

- hide source image links or make them very subtle
- do not show internal numbering on the card face
- do not show border-color metadata on the card face
- long titles should be handled more elegantly
- card titles should feel more like the original deck layout
- the main focus should be the drawn card experience, not the catalog view

## Suggested Next Build

1. Replace the current catalog grid with a single-card draw flow.
2. Add a question input and a draw button.
3. Animate shuffling / random selection.
4. Show the drawn card full screen or in a strong card panel.
5. Show a short explanation, guidance, and optional reflection prompt.
6. Make the layout responsive for mobile first.
7. Keep the database behind the scenes as the deck source.

## Data Model Hint

Keep using the existing JSON database, but the game layer should probably add:

- `drawId`
- `question`
- `drawnCardId`
- `readingText`
- `timestamp`

## Caution

If you keep using the card titles and text from the existing deck, check the copyright situation before publishing publicly. For private use and prototyping, the current structure is fine as a working draft.
