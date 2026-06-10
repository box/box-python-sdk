"""``setup-wizard`` — first-run / repair wizard for box-python-sdk-gen.

Picker-driven, idempotent. Three steps:

1. **Python + dependencies preflight** — verifies Python 3.8+, pip, and
   that ``box_sdk_gen`` is importable. Optionally runs
   ``pip install -e .[test,dev]``.
2. **Auth credentials** — pick one of Developer Token / JWT / Client
   Credentials / OAuth, then capture the credentials it needs and write
   them to ``.env`` at the repo root.
3. **Smoke test snippet** — print a short Python program the user can
   run to verify their setup talks to Box (``client.users.get_user_me()``).

Re-running is safe. The wizard writes only ``.env`` (gitignored).

Run from the repo root::

    ./scripts/setup
    ./scripts/doctor   # read-only audit afterwards

Built using `setup-wizard-squared
<https://github.com/NatalieNobile/setup-wizard-squared>`_ — see that
repo's ``reference/patterns.md`` for design rationale. The package is
named ``dev_setup/`` (not ``setup/``) to avoid colliding with
``setup.py`` and ``setuptools.find_packages()``.
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from . import checks
from . import config as cfg
from .prompts import (
    ask,
    ask_secret,
    banner,
    paced_print,
    pick_steps,
    print_results,
    progress_watch,
    step,
    yes_no,
)

WIZARD_TITLE: str = "Box Python SDK setup"
WIZARD_TAGLINE: str = (
    "Walks you through verifying Python + pip, installing the SDK in\n"
    "editable mode, picking an auth mode, and capturing credentials.\n"
    "Re-running is always safe — every step skips work already done."
)

COMPLETION_FOOTER_LINES: list[str] = [
    "  Health check:    ./scripts/doctor",
    "  Auth docs:       docs/authentication.md",
    "  Wizard flows:    WIZARD_FLOWS.md",
    f"  Mint a token:    {cfg.DEV_CONSOLE_URL}",
]


# ---- subprocess runners -------------------------------------------------


def _run_interactive(
    args: list[str],
    *,
    timeout: int | None = None,
    env: dict[str, str] | None = None,
) -> int:
    """Run a command with the user's TTY connected.

    ``env`` overrides subprocess environment when provided. Build it by
    copying ``os.environ`` and layering ``.env`` values on top so child
    commands see ``BOX_*`` variables even if the user never sourced
    ``.env`` in their shell.
    """
    print(f"  $ {' '.join(args)}")
    try:
        return subprocess.run(args, check=False, timeout=timeout, env=env).returncode
    except FileNotFoundError:
        print(f"  !! {args[0]} not found on PATH; skipping.")
        return 127


# ---- step 1: preflight + dependency install -----------------------------


def step_preflight() -> bool:
    """Verify Python + pip, optionally install dev dependencies."""
    step(1, len(WIZARD_STEPS), "Python + dependencies preflight")
    print("  Verifies Python is recent enough and the SDK installs cleanly.")
    print()
    py = checks.check_python()
    pip_ = checks.check_pip()
    print_results(py + pip_, show_ok=True)
    if any(r.severity == "fail" for r in py + pip_):
        return False

    sdk = checks.check_sdk_importable()
    print_results(sdk, show_ok=True)
    if all(r.severity == "ok" for r in sdk):
        return True

    print()
    paced_print(
        "  The SDK isn't importable yet. Install it in editable mode so",
        "  changes you make show up immediately:",
        f"    {sys.executable} -m pip install -e .[test,dev]",
        after_ms=200,
    )
    print()
    if not yes_no("Run `pip install -e .[test,dev]` now?", default=True):
        print("  Skipped. Install manually when ready, then re-run ./scripts/doctor.")
        return True

    with progress_watch("installing SDK in editable mode (pip)"):
        rc = _run_interactive(
            [sys.executable, "-m", "pip", "install", "-e", ".[test,dev]"]
        )
    if rc != 0:
        print("  [FAIL] pip install exited non-zero. See output above.")
        return False
    paced_print("  → install complete.", after_ms=150)
    return True


# ---- step 2: auth credentials -------------------------------------------


_AUTH_MODE_LABELS: dict[str, str] = {
    cfg.AUTH_MODE_DEV_TOKEN: "Developer Token",
    cfg.AUTH_MODE_JWT: "JWT",
    cfg.AUTH_MODE_CCG: "Client Credentials Grant (CCG)",
    cfg.AUTH_MODE_OAUTH: "OAuth 2.0",
}


def _pick_auth_mode() -> str | None:
    """Inline mini-picker for auth mode. Returns mode string or None."""
    paced_print(
        "  Which auth mode are you setting up?",
        "",
        "    1. Developer Token  — fastest; 60-min TTL; testing only",
        "    2. JWT              — server-to-server; needs config.json from devconsole",
        "    3. Client Credentials — server-to-server; client ID + secret",
        "    4. OAuth 2.0        — end-user app; client ID + secret + redirect URI",
        after_ms=200,
    )
    map_choice = {
        "1": cfg.AUTH_MODE_DEV_TOKEN,
        "2": cfg.AUTH_MODE_JWT,
        "3": cfg.AUTH_MODE_CCG,
        "4": cfg.AUTH_MODE_OAUTH,
    }
    while True:
        raw = ask("Choice", default="1").strip()
        if raw in map_choice:
            return map_choice[raw]
        if raw == "":
            return None
        print(f"  Pick 1, 2, 3, or 4 (got {raw!r}). Try again, or empty to skip.")


def _collect_developer_token() -> bool:
    paced_print(
        "  Mint a Developer Token:",
        f"    {cfg.DEV_CONSOLE_URL}",
        "  → Open your app's configuration page → 'Generate Developer Token'",
        "    → copy the value (it's shown once).",
        "",
        "  Tokens expire after 60 minutes; re-run this step for a fresh one.",
        after_ms=250,
    )
    token = ask_secret("Developer Token", hint="not echoed; ~64-char alphanumeric")
    if not token:
        print("  Skipped — no token entered.")
        return False
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_AUTH_MODE", cfg.AUTH_MODE_DEV_TOKEN)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_DEVELOPER_TOKEN", token)
    paced_print(f"  → wrote {cfg.BOX_ENV_FILE.name}", after_ms=150)
    return True


def _collect_jwt_config() -> bool:
    paced_print(
        "  JWT auth reads a JSON config the developer console exports.",
        f"  Setup guide: {cfg.JWT_AUTH_DOCS_URL}",
        "",
        "  → In the developer console, open your JWT-enabled app →",
        "    Configuration → Add and Manage Public Keys → Generate Keypair.",
        "    The browser downloads config.json. Save it somewhere durable",
        "    (outside the repo if you can — it's a private key).",
        after_ms=300,
    )
    default = str(cfg.DEFAULT_JWT_CONFIG_PATH)
    raw = ask("Path to JWT config JSON", default=default)
    p = Path(raw).expanduser()
    if not p.exists():
        print(f"  [WARN] {p} doesn't exist yet. Saving the path anyway —")
        print("         re-run ./scripts/doctor once the file's in place to validate.")
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_AUTH_MODE", cfg.AUTH_MODE_JWT)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_JWT_CONFIG_PATH", str(p))
    paced_print(f"  → wrote {cfg.BOX_ENV_FILE.name}", after_ms=150)
    return True


def _collect_ccg_creds() -> bool:
    paced_print(
        "  Client Credentials Grant uses client ID + secret to mint tokens.",
        f"  Setup: {cfg.CCG_DOCS_URL}",
        "",
        "  CCG can act as the Service Account (enterpriseID) OR a specific",
        "  user (userID), depending on what the app's authorized for.",
        after_ms=250,
    )
    client_id = ask("Client ID", hint="from devconsole → Configuration").strip()
    client_secret = ask_secret("Client Secret", hint="not echoed")
    if not (client_id and client_secret):
        print("  Skipped — client ID or secret empty.")
        return False
    subject_kind = ask(
        "Subject", hint="`enterprise` for service account, `user` for user-based",
        default="enterprise",
    ).strip().lower()
    if subject_kind not in {"enterprise", "user"}:
        print(f"  Unrecognized subject `{subject_kind}`; defaulting to enterprise.")
        subject_kind = "enterprise"
    subject_id = ask(
        f"{subject_kind.capitalize()} ID",
        hint="numeric (EID for enterprise, UID for user)",
    ).strip()
    if not subject_id:
        print("  Skipped — subject ID empty.")
        return False
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_AUTH_MODE", cfg.AUTH_MODE_CCG)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_CCG_CLIENT_ID", client_id)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_CCG_CLIENT_SECRET", client_secret)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_CCG_SUBJECT_KIND", subject_kind)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_CCG_SUBJECT_ID", subject_id)
    paced_print(f"  → wrote {cfg.BOX_ENV_FILE.name}", after_ms=150)
    return True


def _collect_oauth_creds() -> bool:
    paced_print(
        "  OAuth 2.0 is for apps that ask end-users to grant Box access.",
        f"  Setup: {cfg.OAUTH_DOCS_URL}",
        "",
        "  You'll need client ID, client secret, and a redirect URI",
        "  registered in the developer console.",
        after_ms=250,
    )
    client_id = ask("Client ID", hint="from devconsole → Configuration").strip()
    client_secret = ask_secret("Client Secret", hint="not echoed")
    if not (client_id and client_secret):
        print("  Skipped — client ID or secret empty.")
        return False
    redirect = ask(
        "Redirect URI",
        hint="must match what's registered in the devconsole",
        default="http://localhost:8080/callback",
    ).strip()
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_AUTH_MODE", cfg.AUTH_MODE_OAUTH)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_OAUTH_CLIENT_ID", client_id)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_OAUTH_CLIENT_SECRET", client_secret)
    cfg.write_dotenv_key(cfg.BOX_ENV_FILE, "BOX_OAUTH_REDIRECT_URI", redirect)
    paced_print(f"  → wrote {cfg.BOX_ENV_FILE.name}", after_ms=150)
    return True


def step_auth_credentials() -> bool:
    """Pick an auth mode and capture credentials. Mode lives in BOX_AUTH_MODE."""
    step(2, len(WIZARD_STEPS), "Auth credentials")
    print("  Picks an auth mode and captures the credentials it needs.")
    print()
    existing = cfg.read_dotenv(cfg.BOX_ENV_FILE) if cfg.BOX_ENV_FILE.exists() else {}
    current_mode = existing.get("BOX_AUTH_MODE", "").strip()
    if current_mode:
        label = _AUTH_MODE_LABELS.get(current_mode, current_mode)
        paced_print(f"  Existing auth mode: {label}", after_ms=150)
        if not yes_no("Re-collect / change auth mode?", default=False):
            return True
        print()

    mode = _pick_auth_mode()
    if mode is None:
        print("  Skipped.")
        return True
    print()

    if mode == cfg.AUTH_MODE_DEV_TOKEN:
        return _collect_developer_token()
    if mode == cfg.AUTH_MODE_JWT:
        return _collect_jwt_config()
    if mode == cfg.AUTH_MODE_CCG:
        return _collect_ccg_creds()
    if mode == cfg.AUTH_MODE_OAUTH:
        return _collect_oauth_creds()
    return False


# ---- step 3: smoke test snippet -----------------------------------------


def step_smoke_test() -> bool:
    """Print a copy-pasteable Python snippet that calls users.get_user_me()."""
    step(3, len(WIZARD_STEPS), "Smoke test snippet")
    print("  A 6-line Python program that authenticates and prints your name.")
    print()

    if not cfg.BOX_ENV_FILE.exists():
        paced_print(
            "  [WARN] no .env yet — pick step 2 (Auth credentials) first,",
            "         then re-run setup and pick step 3.",
            after_ms=200,
        )
        return True

    values = cfg.read_dotenv(cfg.BOX_ENV_FILE)
    mode = values.get("BOX_AUTH_MODE", "").strip()
    label = _AUTH_MODE_LABELS.get(mode, "(unknown)")
    paced_print(
        f"  Auth mode in {cfg.BOX_ENV_FILE.name}: {label}",
        "",
        "  Drop this into a .py file at the repo root (or any project that",
        "  has box-sdk-gen on its sys.path):",
        "",
        after_ms=150,
    )

    if mode == cfg.AUTH_MODE_DEV_TOKEN:
        token = values.get("BOX_DEVELOPER_TOKEN", "")
        preview = token[:8] + "…" if len(token) > 8 else "<TOKEN>"
        print('    import os')
        print('    from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth')
        print('')
        print(f'    auth = BoxDeveloperTokenAuth(token=os.environ["BOX_DEVELOPER_TOKEN"])  # or "{preview}"')
        print('    client = BoxClient(auth=auth)')
        print('    me = client.users.get_user_me()')
        print('    print("Hello,", me.name)')
        print()
        print("    Run after `set -a; source .env; set +a` (or `python-dotenv` etc).")
    elif mode == cfg.AUTH_MODE_JWT:
        path = values.get("BOX_JWT_CONFIG_PATH", "<PATH>")
        print('    from box_sdk_gen import BoxClient, BoxJWTAuth, JWTConfig')
        print('')
        print(f'    config = JWTConfig.from_config_file({path!r})')
        print('    auth = BoxJWTAuth(config=config)')
        print('    client = BoxClient(auth=auth)')
        print('    print("Hello,", client.users.get_user_me().name)')
    elif mode == cfg.AUTH_MODE_CCG:
        kind = values.get("BOX_CCG_SUBJECT_KIND", "enterprise")
        sid = values.get("BOX_CCG_SUBJECT_ID", "<ID>")
        print('    import os')
        print('    from box_sdk_gen import BoxClient, BoxCCGAuth, CCGConfig')
        print('')
        if kind == "enterprise":
            print('    config = CCGConfig(')
            print('        client_id=os.environ["BOX_CCG_CLIENT_ID"],')
            print('        client_secret=os.environ["BOX_CCG_CLIENT_SECRET"],')
            print(f'        enterprise_id="{sid}",')
            print('    )')
        else:
            print('    config = CCGConfig(')
            print('        client_id=os.environ["BOX_CCG_CLIENT_ID"],')
            print('        client_secret=os.environ["BOX_CCG_CLIENT_SECRET"],')
            print(f'        user_id="{sid}",')
            print('    )')
        print('    auth = BoxCCGAuth(config=config)')
        print('    client = BoxClient(auth=auth)')
        print('    print("Hello,", client.users.get_user_me().name)')
    elif mode == cfg.AUTH_MODE_OAUTH:
        print('    import os')
        print('    from box_sdk_gen import BoxClient, BoxOAuth, OAuthConfig')
        print('')
        print('    config = OAuthConfig(')
        print('        client_id=os.environ["BOX_OAUTH_CLIENT_ID"],')
        print('        client_secret=os.environ["BOX_OAUTH_CLIENT_SECRET"],')
        print('    )')
        print('    auth = BoxOAuth(config=config)')
        print('    # Then run the OAuth flow — see docs/authentication.md.')
    else:
        print("    (see docs/authentication.md for the snippet matching your mode)")

    print()
    paced_print(
        "  Run it from the repo root with the SDK on sys.path:",
        "    python3 smoke.py",
        "",
        "  Or use python-dotenv to auto-load .env:",
        "    pip install python-dotenv",
        "    python3 -c \"from dotenv import load_dotenv; load_dotenv(); exec(open('smoke.py').read())\"",
        after_ms=200,
    )
    return True


# ---- step registry ------------------------------------------------------

WizardStepFn = Callable[[], bool]
WIZARD_STEPS: list[tuple[str, str, bool, WizardStepFn]] = [
    ("preflight", "Python + dependencies preflight", True, step_preflight),
    ("auth", "Auth credentials (Developer Token / JWT / CCG / OAuth)", True, step_auth_credentials),
    ("smoke", "Smoke test snippet", True, step_smoke_test),
]


# ---- runner -------------------------------------------------------------


def run_steps(selected_ids: list[str]) -> int:
    if not selected_ids:
        paced_print("  Nothing selected. Exiting.", after_ms=200)
        return 0

    paced_print(
        f"  → Will set up: {', '.join(sid for sid in selected_ids)}",
        after_ms=200,
    )

    failures: list[str] = []
    for sid, _label, _recommended, fn in WIZARD_STEPS:
        if sid not in selected_ids:
            continue
        try:
            ok = fn()
        except KeyboardInterrupt:
            print("\n  Interrupted by user.")
            return 130
        except Exception as exc:  # noqa: BLE001 - wizard must stay friendly
            print(f"  [FAIL] step `{sid}` raised {type(exc).__name__}: {exc}")
            failures.append(sid)
            continue
        if not ok:
            failures.append(sid)

    print()
    banner(f"{WIZARD_TITLE} complete")
    for line in COMPLETION_FOOTER_LINES:
        paced_print(line, after_ms=80)

    if failures:
        print()
        print(f"  {len(failures)} step(s) reported issues: {', '.join(failures)}")
        print("  Re-run `./scripts/setup` and pick those steps to retry.")
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])

    banner(WIZARD_TITLE)
    paced_print(*WIZARD_TAGLINE.splitlines(), after_ms=300)
    print()

    picker_items = [(sid, label, recommended) for sid, label, recommended, _ in WIZARD_STEPS]
    selected = pick_steps(picker_items)
    print()

    return run_steps(selected)


if __name__ == "__main__":
    raise SystemExit(main())
