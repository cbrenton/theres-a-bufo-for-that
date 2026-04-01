# there's a bufo for that

A browser for custom emoji. Search across all words in emoji names — not just prefixes — so you can find `bufo-goes-to-jail` by typing `jail`.

## Usage

```bash
uv run server.py                     # serves ./bufos/ on port 8000
uv run server.py /path/to/emojis     # custom emoji directory
uv run server.py /path/to/emojis --port 9000
```

Open `http://localhost:8000` in your browser.

## Search

Type any word from an emoji name. Multi-word queries narrow the results (space-separated). Examples:

- `jail` → finds `big-bufo-goes-to-jail`
- `pull request` → finds `smol-bufo-has-a-smol-pull-request-...`

Clicking an emoji copies `:emoji-name:` to your clipboard, ready to paste into Slack/Zulip.

## Setup

Drop your org's emoji images into a directory (any mix of `.png`, `.jpg`, `.gif`, `.webp`) and point the server at it. Filenames become the emoji names.
