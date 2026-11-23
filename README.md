# Ergo Sum: AI Philosophy Digest

Weekly digest of public writing on the philosophy of AI (consciousness, alignment, human-AI
collaboration, society) plus AI in medical education. Fetches Substack/blog RSS, Bluesky, PubMed and
arXiv; Claude selects, clusters and synthesizes; output goes to a static archive (`docs/`, GitHub Pages)
and an email via Buttondown.

## Run locally
    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    .venv/bin/python digest.py --dry-run     # fetch only
    .venv/bin/python digest.py               # full run (uses `claude` CLI login, or ANTHROPIC_API_KEY)

## Secrets (GitHub repo > Settings > Secrets and variables > Actions)
- `CLAUDE_CODE_OAUTH_TOKEN` — from `claude setup-token` (uses your Claude subscription)
- `BUTTONDOWN_API_KEY` — Buttondown > Settings > API
- `BSKY_HANDLE`, `BSKY_APP_PASSWORD` — optional; use a Bluesky *app password*, never the main password
- Repo variable `SEND_MODE`: leave unset for drafts; set to `now` to send automatically.

Edit `config.yaml` to change sources and topic scope.
