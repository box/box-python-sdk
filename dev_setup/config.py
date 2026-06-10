"""Paths and small config helpers shared by the wizard and doctor.

Discovers the target repo root relative to this file so the package
works no matter where the user invokes it from. Per-user state lives
in ``~/.<project>/`` (overridable via ``$WIZARD_STATE_DIR``) so the
wizard never writes per-machine state into the git checkout.

Customization checklist when porting to a new repo:

1. Update ``PROJECT_NAME`` to whatever short name you want for the
   ``~/.<project>/`` state dir.
2. Decide where ``parents[N]`` should land — the scaffold assumes the
   ``setup/`` package sits one directory below the repo root. If you
   nest deeper (e.g. ``scripts/setup/``), bump the index.
3. Add module-level constants for any well-known config files the
   wizard creates (``BOX_CONFIG_FILE``, ``LOCAL_PROPERTIES``, etc.).
   Mirror the ``ZD_ENV_FILE`` / ``PAT_ENV_FILE`` shape from bq_ranger:
   accept an env-var override so tests can swap paths.
4. Drop any constants you don't need. There's no charge for empty
   space here — the file should be small.
"""

from __future__ import annotations

import os
from pathlib import Path

# ---- repo + state -------------------------------------------------------

PROJECT_NAME: str = "box-python-sdk-gen"

# REPO_ROOT discovery. Adjust the parents[N] depth to match where you
# install the setup package. Default: setup/ sits at <repo>/setup/, so
# parents[1] resolves to <repo>.
REPO_ROOT: Path = Path(__file__).resolve().parents[1]

# Per-user state directory (created lazily, never at import time so
# read-only callers don't trigger a filesystem mutation just by
# importing this module).
_STATE_DIR_ENV = f"{PROJECT_NAME.upper().replace('-', '_')}_STATE_DIR"
STATE_DIR: Path = Path(
    os.environ.get(_STATE_DIR_ENV, str(Path.home() / f".{PROJECT_NAME}"))
).expanduser()


def ensure_state_dir() -> Path:
    """Create ``STATE_DIR`` if missing and return it.

    Lazy so read-only callers (the doctor, ad-hoc imports in CI or
    sandboxed environments without a writable ``$HOME``) don't trigger
    a filesystem mutation just by importing the package. Idempotent.
    """
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR


# ---- Box-specific config files ------------------------------------------
#
# The wizard writes one ``.env`` at the repo root with the user's chosen
# auth mode and credentials. ``.env`` is the Python ecosystem's default
# convention; the wizard's ``read_dotenv``/``write_dotenv_key`` helpers
# parse it natively.
#
# JWT auth uses an additional JSON config file (the one the developer
# console exports). The wizard records its absolute path in ``.env``
# under ``BOX_JWT_CONFIG_PATH``.

BOX_ENV_FILE: Path = Path(
    os.environ.get("BOX_SDK_DOTENV", str(REPO_ROOT / ".env"))
).expanduser()

BOX_ENV_EXAMPLE: Path = REPO_ROOT / ".env.example"

DEFAULT_JWT_CONFIG_PATH: Path = Path(
    os.environ.get("BOX_JWT_CONFIG_PATH", str(REPO_ROOT / "box-jwt-config.json"))
).expanduser()

# URLs printed in the token-entry prompts so the user knows where to
# mint each credential. Centralized so docs + wizard cite the same
# canonical pages.
DEV_CONSOLE_URL: str = "https://app.box.com/developers/console"
JWT_AUTH_DOCS_URL: str = (
    "https://developer.box.com/guides/authentication/jwt/jwt-setup/"
)
OAUTH_DOCS_URL: str = (
    "https://developer.box.com/guides/authentication/oauth2/"
)
CCG_DOCS_URL: str = (
    "https://developer.box.com/guides/authentication/client-credentials/"
)

# Minimum required Python (matches setup.py classifiers).
MIN_PYTHON: tuple[int, int] = (3, 8)

# Auth mode constants. Stored verbatim in .env under BOX_AUTH_MODE and
# consumed by the smoke-test step.
AUTH_MODE_DEV_TOKEN: str = "developer_token"
AUTH_MODE_JWT: str = "jwt"
AUTH_MODE_CCG: str = "ccg"
AUTH_MODE_OAUTH: str = "oauth"

ALL_AUTH_MODES: tuple[str, ...] = (
    AUTH_MODE_DEV_TOKEN,
    AUTH_MODE_JWT,
    AUTH_MODE_CCG,
    AUTH_MODE_OAUTH,
)


# ---- dotenv helpers -----------------------------------------------------


def read_dotenv(path: Path) -> dict[str, str]:
    """Parse a tiny .env-style file into a dict.

    Handles ``KEY=value`` and ``KEY="value"`` / ``KEY='value'``. Ignores
    blank lines and ``#`` comments. Does NOT support multiline values,
    backslash escapes, or shell expansion — kept intentionally minimal
    so we don't pull in python-dotenv as a dependency.
    """
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip()
        if (len(v) >= 2) and (v[0] == v[-1]) and v[0] in ("'", '"'):
            v = v[1:-1]
        out[k] = v
    return out


def write_dotenv_key(path: Path, key: str, value: str) -> None:
    """Idempotently set ``key=value`` in a tiny .env file.

    Creates the file if missing, replaces an existing key in place, or
    appends if the key isn't there yet. Quotes the value with double
    quotes if it contains a space, ``#``, or ``=`` so the same parser
    that wrote it can read it back.

    Sets owner-only (0600) permissions on POSIX systems — best-effort
    on Windows / unusual filesystems where chmod isn't supported.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_quote = any(c in value for c in (" ", "#", "="))
    safe_value = value.replace('"', r"\"") if needs_quote else value
    rendered = f'{key}="{safe_value}"' if needs_quote else f"{key}={value}"

    if not path.exists():
        path.write_text(rendered + "\n", encoding="utf-8")
        chmod_owner_only(path)
        return

    lines = path.read_text(encoding="utf-8").splitlines()
    replaced = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(f"{key}="):
            lines[i] = rendered
            replaced = True
            break
    if not replaced:
        lines.append(rendered)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    chmod_owner_only(path)


def chmod_owner_only(path: Path) -> None:
    """Best-effort owner-only (0600) permissions for local secrets.

    Windows and some network filesystems don't support POSIX modes.
    The write still succeeded — keep setup flowing and lean on the
    docs to call out platform-specific hardening if needed.
    """
    try:
        path.chmod(0o600)
    except OSError:
        pass


def atomic_write_text(path: Path, content: str, *, mode: int = 0o644) -> None:
    """Write ``content`` to ``path`` atomically.

    Writes to a sibling tempfile, then ``os.replace`` to swap it in.
    Avoids leaving a half-written secrets file if the process is killed
    mid-write. ``mode`` is best-effort (skipped on filesystems without
    POSIX permissions).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    try:
        tmp.chmod(mode)
    except OSError:
        pass
    os.replace(tmp, path)
