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
- The Actions workflow is manual-only (`workflow_dispatch`); the weekly schedule runs from the Mac (see below).

Edit `config.yaml` to change sources and topic scope.

## Running from a Mac instead of GitHub Actions
Substack intermittently 403s GitHub's servers, so sends run from a Mac via launchd
(login + daily 08:00, which also fires on wake if missed; `scripts/run_if_due.py` only sends if >= 6 days since the last success and tries at most once a day).
1. Create `~/.ergo-sum/env` (chmod 600) with `BUTTONDOWN_API_KEY=...` and optionally `BSKY_HANDLE`, `BSKY_APP_PASSWORD`.
2. `bash scripts/install_launchd.sh`
3. State: `~/.ergo-sum/last_send` (delete it, and `last_attempt`, to force the next run). Log: `~/.ergo-sum/run.log`.
