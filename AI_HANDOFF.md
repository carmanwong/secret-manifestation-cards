# AI Handoff: Secret Manifestation Cards

## Branch To Use

If you are another AI or developer picking this up, start from:

- `card-result-background-only`

That is the current preferred publish branch.

Do not assume `main`, `ritual-game-redesign`, or other experiment branches reflect the preferred user-facing version.

## Current Approved UX

The user currently prefers:

- the older front page layout style
- the older library layout style
- Traditional Chinese UI
- the reveal card page to stay mostly dark
- only a subtle warm glow on the reveal page background

The reveal page background should not become the main visual focus.
The card itself remains the main focus.

## Files That Matter

- `index.html`
  Redirect entry for GitHub Pages
- `secret_oracle_v6.html`
  Current app UI and interaction logic
- `database/cards.json`
  Current card content source of truth
- `database/cards.csv`
  CSV export
- `database/cards.sqlite`
  SQLite export

## Important Content Notes

- Keep original card wording unless the user explicitly asks to correct or restore a specific card.
- The card `SMC-007` / `意念會化為現實` was explicitly restored and should remain:

  你想要什麼就告訴宇宙，
  只要想著你要什麼就行了。
  然後宇宙會立刻安排人物、狀況、事件，
  來讓你得到它。
  你唯一的工作就是在心裡一直想著，
  直到它到你手中為止。

- Do not casually rewrite card text just to fix wrapping. Fix layout first.

## UI Guardrails

- Do not redesign the front page unless the user explicitly asks.
- Do not swap button assets casually; the user is sensitive to unintended English/Chinese regressions.
- Do not make reveal-page background treatments too obvious.
- Avoid adding large new controls unless requested.

## Hosting Notes

The simplest publish path is GitHub Pages from:

- branch: `card-result-background-only`
- folder: `/ (root)`

Because `index.html` exists, the shared root URL can open directly.

## Safe Next Changes

- small reveal-page typography tuning
- card content corrections when explicitly provided by the user
- hosting setup / Pages publishing
- subtle spacing fixes

## Changes To Avoid Without Permission

- front page redesign
- library redesign
- replacing Chinese assets with English ones
- major reveal-page restyling
