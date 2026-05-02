# The Secret Manifestation Cards

An interactive Traditional Chinese manifestation card web app based on the collected card text from "The Secret" card deck.

## Publish Version

The current family-and-friends share version is on the branch:

- `card-result-background-only`

That version keeps:

- the preferred front page layout
- the preferred library layout
- a dark reveal page with only a subtle warm glow in the background
- updated card data loaded from `database/cards.json`

## Main Files

- `index.html`: GitHub Pages entry point
- `secret_oracle_v6.html`: current app file
- `database/cards.json`: source of truth for card titles and text
- `AI_HANDOFF.md`: notes for future AI/developer updates

## Local Run

Open `secret_oracle_v6.html` directly, or run a simple local server and visit:

- `http://127.0.0.1:8000/secret_oracle_v6.html`

## GitHub Pages

For public sharing, publish from the `card-result-background-only` branch and root folder.

If `index.html` is used as the Pages entry, the root site URL will work directly without typing `secret_oracle_v6.html`.
