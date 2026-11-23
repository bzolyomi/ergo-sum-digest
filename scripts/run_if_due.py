#!/usr/bin/env python3
"""Run the weekly digest from this Mac if one is due. Safe to call as often as you like.

Triggered by launchd (login + daily 08:00; missed 08:00 runs fire on wake). Exits immediately unless
>= MIN_DAYS have passed since the last *successful* send, and tries at most once per calendar day.
State lives in ~/.ergo-sum/.

Secrets live in ~/.ergo-sum/env (KEY=VALUE per line, chmod 600), never in the repo:
  BUTTONDOWN_API_KEY, and optionally BSKY_HANDLE, BSKY_APP_PASSWORD.
The Claude call uses your local `claude` login, so no token is needed here.
"""
import datetime as dt
import fcntl
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".ergo-sum"
STATE = STATE_DIR / "last_send"
ATTEMPT = STATE_DIR / "last_attempt"
ENV = STATE_DIR / "env"
MIN_DAYS = 6


def log(msg):
    print(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def notify(msg):
    subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "Ergo Sum digest"'],
                   check=False)


def load_env():
    if not ENV.exists():
        sys.exit(f"Missing {ENV}")
    for line in ENV.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip("'\"")


def due():
    if not STATE.exists():
        return True
    last = dt.date.fromisoformat(STATE.read_text().strip())
    return (dt.date.today() - last).days >= MIN_DAYS


def wait_for_network(timeout=300):
    end = time.time() + timeout
    while time.time() < end:
        try:
            urllib.request.urlopen("https://api.buttondown.com", timeout=10)
            return True
        except urllib.error.HTTPError:
            return True  # reachable (any HTTP response means the network is up)
        except Exception:
            time.sleep(15)
    return False


def sh(*cmd):
    return subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)


def main():
    STATE_DIR.mkdir(exist_ok=True)
    lock = open(STATE_DIR / "lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return  # another trigger is already running
    if not due():
        return
    if ATTEMPT.exists() and ATTEMPT.read_text().strip() == dt.date.today().isoformat():
        return  # already tried today (and failed); try again tomorrow
    log("Digest is due.")
    load_env()
    if not wait_for_network():
        log("No network; will retry on next trigger.")
        return

    ATTEMPT.write_text(dt.date.today().isoformat())
    sh("git", "pull", "--rebase", "origin", "main")  # pick up any code/archive changes
    r = subprocess.run([str(REPO / ".venv/bin/python"), "digest.py", "--send", "now"],
                       cwd=REPO, text=True, capture_output=True, timeout=1800)
    print(r.stderr[-3000:], flush=True)
    if r.returncode != 0:
        log("Digest FAILED; will retry tomorrow.")
        notify("Digest failed — see ~/.ergo-sum/run.log")
        return
    # Record success immediately so a later git failure can never cause a duplicate email.
    STATE.write_text(dt.date.today().isoformat())
    log("Email sent.")

    sh("git", "add", "docs")
    if sh("git", "diff", "--cached", "--quiet").returncode != 0:
        sh("git", "commit", "-m", "Add weekly digest")
        p = sh("git", "push", "origin", "main")
        if p.returncode != 0:
            log(f"Archive push failed: {p.stderr[-500:]}")
            notify("Email sent, but archive push failed")
        else:
            log("Archive pushed.")


if __name__ == "__main__":
    main()
