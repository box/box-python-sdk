"""TTY helpers for the wizard and doctor.

Stdlib-only. Centralized here so the wizard and doctor render identically —
the user gets the same ``[OK]`` / ``[WARN]`` / ``[FAIL]`` glyphs and the
same fix-hint formatting from both tools.

This is part of the ``setup-wizard-squared`` scaffold. Drop the file
into a target repo's ``setup/`` package and customize ``wizard.py``;
``prompts.py`` itself shouldn't usually need editing per repo.

Tunables:
    ``WIZARD_PACE_MS=<int>`` — per-line pause when pacing framing text.
        Default 80ms. ``0`` disables pacing. Auto-disabled when stdout
        isn't a TTY.
"""

from __future__ import annotations

import contextlib
import os
import sys
import threading
import time
from collections.abc import Iterable, Iterator
from typing import Literal

# Import readline so input() supports arrow-key line editing and history
# instead of inserting raw escape codes (^[[A / ^[[B). On macOS, Python's
# stdlib readline links against libedit rather than GNU readline; on
# Windows the module isn't shipped — input() still works, just without
# the line editor.
try:
    import readline  # noqa: F401  -- side-effect import (enables line editing)
except ImportError:
    pass

from .checks import CheckResult

Severity = Literal["ok", "warn", "fail"]

_GLYPH = {"ok": "[OK]  ", "warn": "[WARN]", "fail": "[FAIL]"}

# ---- pacing -------------------------------------------------------------
#
# Sectional pacing: small inter-line pauses inside framing blocks
# (banners, step intros, completion summaries) plus a longer settle
# pause AFTER each block. Status rows, prompts, and command output stay
# instant so the wizard never feels frozen.
#
# Tuning: WIZARD_PACE_MS=<int> overrides the default per-line ms.
#   0      -> pacing disabled (same as non-TTY).
#   80     -> default; calm but not slow.
#   200+   -> deliberate / dramatic for live demos or first-time users.
# Auto-disabled when stdout isn't a TTY (CI, piped output, capture).

_DEFAULT_PACE_MS = 80
_PACE_ENV_VAR = "WIZARD_PACE_MS"


def _pace_ms() -> int:
    """Resolve effective per-line pause in ms; 0 disables pacing."""
    if not sys.stdout.isatty():
        return 0
    raw = os.environ.get(_PACE_ENV_VAR)
    if raw is None:
        return _DEFAULT_PACE_MS
    try:
        v = int(raw)
    except ValueError:
        return _DEFAULT_PACE_MS
    return max(0, v)


def paced_print(*lines: str, pause_ms: int | None = None, after_ms: int = 0) -> None:
    """Print each line with the per-line pause between, then sleep ``after_ms``.

    Use for FRAMING text — banners, step intros, completion summaries.
    Don't pace status rows, command output, or prompt text: pacing
    those makes the wizard feel slow without aiding reading.

    ``pause_ms`` overrides the global per-line rate FOR THIS CALL ONLY.
    Use it to slow-roll a long prose block ("Star Wars crawl" feel) so
    a multi-paragraph explainer scrolls in one breath instead of dumping
    all at once. Typical values:

       None  -> use global WIZARD_PACE_MS (default 80ms, snappy)
       150   -> slower scroll for paragraph prose
       250   -> deliberate "read this carefully" rhythm

    The global kill switch (``WIZARD_PACE_MS=0`` or non-TTY) still wins —
    passing ``pause_ms`` does NOT force pacing on when it would otherwise
    be off.

    ``after_ms`` is the sectional settle pause that separates this block
    from whatever prints next (a prompt, a status row, the next framing
    block). Typical values:

       0    -> no settle (block flows directly into the next line)
       200  -> short settle (after a step completion line)
       400  -> banner settle (give the user a beat to read it)
    """
    pace = _pace_ms()
    if pace and pause_ms is not None:
        pace = max(0, pause_ms)
    last = len(lines) - 1
    for i, line in enumerate(lines):
        print(line)
        if pace and i < last:
            time.sleep(pace / 1000)
    if pace and after_ms > 0:
        time.sleep(after_ms / 1000)


def paced_pause(ms: int) -> None:
    """Sleep ``ms`` milliseconds when pacing is enabled; no-op otherwise."""
    pace = _pace_ms()
    if pace and ms > 0:
        time.sleep(ms / 1000)


# ---- progress watchdog --------------------------------------------------
#
# Wrap subprocess calls (or any potentially-slow block) so the user gets
# a "current action: <X>" status line if the wrapped block goes silent
# for more than a few seconds. Without this, long silent stretches during
# `brew install`, `npm install -g`, dependency syncs, etc. look exactly
# like a hung wizard.
#
# Don't wrap commands that have their own interactive prompts (e.g.
# `gh auth login`'s device-flow prompts, CLIs that ask for tokens) —
# the watcher line interleaves with the active prompt and confuses
# the user. Use this only for silent or progress-streaming subprocesses.

_PROGRESS_THRESHOLD_MS = 5000


@contextlib.contextmanager
def progress_watch(
    description: str,
    *,
    threshold_ms: int = _PROGRESS_THRESHOLD_MS,
) -> Iterator[None]:
    """Print ``current action: <description>`` if the block runs >threshold_ms.

    Use as a context manager around subprocess calls that can stall::

        with progress_watch("installing jira-cli (brew)"):
            rc = _run_interactive(["brew", "install", "jira-cli"])

    A daemon thread sleeps for ``threshold_ms``; if the block hasn't
    exited by then it prints the heads-up line once. On exit, if the
    threshold was crossed, also prints ``done in Ns`` so the user knows
    the silent stretch ended.

    No-op for non-TTY (CI / piped output / capture). Re-entrant: each
    nested level announces independently with its own watcher thread.
    """
    if not sys.stdout.isatty():
        yield
        return

    done = threading.Event()
    crossed = threading.Event()

    def _watch() -> None:
        if not done.wait(threshold_ms / 1000):
            crossed.set()
            print(f"  current action: {description}")

    t = threading.Thread(target=_watch, daemon=True)
    t.start()
    start = time.monotonic()
    try:
        yield
    finally:
        done.set()
        if crossed.is_set():
            elapsed = time.monotonic() - start
            print(f"  → done in {elapsed:.0f}s")


# ---- framing ------------------------------------------------------------


def banner(title: str, *, after_ms: int = 400) -> None:
    """Print a thick bordered title line with a settle pause after."""
    bar = "=" * (len(title) + 4)
    paced_print(bar, f"= {title} =", bar, after_ms=after_ms)


def step(num: int, total: int, title: str) -> None:
    """Print ``--- Step N/T: title ---`` with a leading blank + settle pause."""
    print()
    paced_print(f"--- Step {num}/{total}: {title} ---", after_ms=200)


# ---- input prompts ------------------------------------------------------


def yes_no(prompt: str, default: bool = True) -> bool:
    """Prompt for yes/no. Empty input picks ``default``.

    Treats EOF / Ctrl-D as "decline" so piping ``echo "" |`` to the
    wizard doesn't accidentally agree to destructive actions.
    """
    suffix = "Y/n" if default else "y/N"
    try:
        raw = input(f"{prompt} ({suffix}): ").strip().lower()
    except EOFError:
        return False
    if not raw:
        return default
    return raw in {"y", "yes"}


def ask(label: str, *, hint: str | None = None, default: str | None = None) -> str:
    """Single-line free-text prompt with optional hint and default."""
    if hint:
        print(f"  ({hint})")
    suffix = f" [{default}]" if default else ""
    try:
        raw = input(f"  {label}{suffix}: ").strip()
    except EOFError:
        return default or ""
    return raw or (default or "")


def ask_secret(label: str, *, hint: str | None = None) -> str:
    """Hidden-input prompt for a token / password / API key.

    Wraps ``getpass.getpass`` so the value doesn't echo to the terminal
    or land in shell history. EOF returns an empty string (caller should
    detect and re-prompt or skip).
    """
    from getpass import getpass

    if hint:
        print(f"  ({hint})")
    try:
        return getpass(f"  {label} (input hidden): ").strip()
    except EOFError:
        return ""


# ---- step picker --------------------------------------------------------
#
# Render a numbered "what would you like to set up?" menu and parse
# the user's response into the set of step ids to run. Lets users
# pick a subset up front instead of being walked through every
# component sequentially.

PickerItem = tuple[str, str, bool]
"""A single menu item: ``(step_id, label, recommended)``.

``step_id`` is the caller's stable identifier (returned in the selection
list). ``label`` is what the user sees on the menu line.
``recommended=True`` tags the item with ``[R]`` and includes it in the
default selection when the user just hits Enter.
"""


def _parse_picker_input(
    raw: str,
    items: list[PickerItem],
    default_ids: list[str],
) -> tuple[list[str] | None, str | None]:
    """Parse picker input into a list of selected step ids.

    Returns ``(selected_ids, None)`` on success or ``(None, error_msg)``
    on parse failure so the caller can re-prompt.

    Accepts:
        - empty string -> ``default_ids``
        - ``"all"`` -> every item id
        - ``"none"`` -> empty list (skip everything)
        - ``"recommended"`` -> ids of items tagged recommended
        - comma-separated 1-based numbers: ``"1,3,5"``
        - inclusive ranges: ``"1-3"``
        - mixed: ``"1-3,5,7"``

    Selected ids are returned in menu order, not input order, so the
    caller can iterate the items list once and run picked entries in
    their canonical sequence.
    """
    raw = raw.strip().lower()
    if not raw:
        return list(default_ids), None
    if raw == "all":
        return [iid for iid, _, _ in items], None
    if raw == "none":
        return [], None
    if raw == "recommended":
        return [iid for iid, _, recommended in items if recommended], None

    selected_indices: set[int] = set()
    for token in raw.replace(" ", "").split(","):
        if not token:
            continue
        if "-" in token:
            try:
                lo_s, hi_s = token.split("-", 1)
                lo, hi = int(lo_s), int(hi_s)
            except ValueError:
                return None, f"bad range `{token}`"
            if lo < 1 or hi > len(items) or lo > hi:
                return None, f"range `{token}` out of bounds (1-{len(items)})"
            selected_indices.update(range(lo, hi + 1))
        else:
            try:
                n = int(token)
            except ValueError:
                return None, f"not a number: `{token}`"
            if n < 1 or n > len(items):
                return None, f"`{n}` out of range (1-{len(items)})"
            selected_indices.add(n)

    return [iid for i, (iid, _, _) in enumerate(items, 1) if i in selected_indices], None


def pick_steps(
    items: list[PickerItem],
    *,
    title: str = "What would you like to set up?",
    indent: str = "  ",
) -> list[str]:
    """Render a numbered picker; return selected step ids in menu order.

    Each entry's ``recommended`` flag shows as a leading ``[R]`` tag and
    determines the default selection when the user just hits Enter. The
    caller iterates its own item list and runs any step whose id is in
    the returned list — this helper doesn't invoke step bodies itself.

    Empty selection (``none`` or no recommended items) is valid and
    returns an empty list; callers should handle that gracefully (e.g.,
    print "skipping all extras" and exit cleanly).

    EOF / Ctrl-D returns the default selection so non-interactive
    invocations (CI, ``echo "" | ...``) don't accidentally pick or skip
    everything.
    """
    default_ids = [iid for iid, _, recommended in items if recommended]

    paced_print(title, after_ms=150)
    print()
    for i, (_, label, recommended) in enumerate(items, 1):
        tag = "[R]" if recommended else "   "
        print(f"{indent}{i}. {tag} {label}")
    print()
    print(f"{indent}Pick: comma-separated numbers (1,3,5), ranges (1-3),")
    print(f"{indent}      `all`, `recommended`, or `none`. [R] = recommended.")

    while True:
        try:
            raw = input(f"{indent}Choice [recommended]: ")
        except EOFError:
            return list(default_ids)

        selected, err = _parse_picker_input(raw, items, default_ids)
        if selected is None:
            print(f"{indent}  invalid input: {err}. Try again.")
            continue
        return selected


# ---- result rendering ---------------------------------------------------


def print_results(
    results: Iterable[CheckResult],
    *,
    show_ok: bool = True,
    show_fix: bool = True,
    indent: str = "  ",
) -> None:
    """Render a sequence of CheckResult.

    By default prints all severities so the doctor's full report is
    visible; set ``show_ok=False`` in the wizard to suppress noise from
    successful steps and only surface the warnings/failures.

    Set ``show_fix=False`` at call sites where the wizard immediately
    follows up with its own multi-line remediation block, so the user
    doesn't see the same fix command twice (once as the terse one-line
    ``fix:`` hint, then again in the prose block). The doctor leaves
    this at the default so its standalone report is fully self-contained.
    """
    for r in results:
        if r.severity == "ok" and not show_ok:
            continue
        glyph = _GLYPH[r.severity]
        print(f"{indent}{glyph} {r.name}: {r.message}")
        if r.fix_hint and r.severity != "ok" and show_fix:
            print(f"{indent}        fix: {r.fix_hint}")
