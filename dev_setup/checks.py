"""Health checks shared by the wizard and doctor.

Every check returns one or more :class:`CheckResult`. The same functions
are called from the wizard (per-step verification) and the doctor (full
report) so validation logic lives in exactly one place. This is the
"doctor-symmetric" principle from ``reference/patterns.md``.

When porting:

1. Replace the example checks at the bottom with your repo's checks.
2. Add a category grouping if you have many checks (the bq_ranger
   reference splits `core` vs `extras` so the doctor can group output).
3. Each check that talks to a network service should accept an optional
   ``timeout`` kwarg — default 10-15s. Long-hung probes break the
   doctor's "fast read-only audit" contract.

Conventions:
    * ``fix_hint`` is required on every ``fail``. The hint must name a
      concrete next action, not generic advice.
    * Checks never prompt. If you need user input, that's a wizard step.
    * Checks are pure read-only audits — they never write files or
      mutate state.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Literal

Severity = Literal["ok", "warn", "fail"]


@dataclass
class CheckResult:
    """One row in the doctor's report.

    ``fix_hint`` is required on every ``fail`` (enforced by convention,
    not the type system). The hint must name the next concrete action —
    "re-run ``./scripts/setup``", not "fix your config".
    """

    name: str
    severity: Severity
    message: str
    fix_hint: str | None = None

    @property
    def ok(self) -> bool:
        return self.severity == "ok"


@dataclass
class DoctorReport:
    """Aggregated checks plus optional structured evidence.

    Add fields here when the wizard needs to consume *typed* values from
    the doctor (e.g. the resolved current-user name, the active project
    id) instead of just severity rows. Keep the field count small —
    most wizards never need more than a half-dozen.
    """

    results: list[CheckResult] = field(default_factory=list)

    @property
    def all_ok(self) -> bool:
        """True iff no check failed (warnings tolerated)."""
        return all(r.severity != "fail" for r in self.results)

    @property
    def any_failures(self) -> bool:
        return any(r.severity == "fail" for r in self.results)

    def add(self, *results: CheckResult) -> None:
        self.results.extend(results)


# ---- generic helpers ----------------------------------------------------


def _run(
    args: list[str],
    *,
    timeout: int = 15,
    input_text: str | None = None,
    env: dict[str, str] | None = None,
) -> tuple[int, str, str]:
    """Run a subprocess and capture ``(returncode, stdout, stderr)``.

    Returns ``(127, "", str(exc))`` if the binary is missing — same
    convention as ``which`` so callers don't need to special-case
    ``FileNotFoundError`` separately from non-zero exit codes. Returns
    ``(124, "", "timed out after Ns")`` on timeout.

    ``env`` lets callers layer dotenv-derived values onto a copy of
    ``os.environ`` so checks against tools that read tokens from env
    (jira-cli, gh, gcloud) work without forcing the user to pre-source.
    """
    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            input=input_text,
            check=False,
            env=env,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except subprocess.TimeoutExpired:
        return 124, "", f"timed out after {timeout}s"


def _on_path(name: str) -> bool:
    """True if ``name`` resolves to an executable on the user's PATH."""
    return shutil.which(name) is not None


def is_ssl_trust_failure(message: str) -> bool:
    """True if ``message`` looks like a TLS trust-store error.

    SSL verification failures aren't credential / config / network
    problems — re-prompting the user for tokens or rerunning the check
    would waste their time. Branch on this so the wizard can route to
    a "fix your trust store" remediation block instead of treating it
    as a generic auth failure.

    Patterns cover every flavor of "I couldn't verify the server cert"
    surfaced by urllib, requests, curl, openssl on macOS / Linux. We
    don't detect *valid* certs rejected for other reasons (expiry,
    hostname mismatch) — those are real network problems and a generic
    "check VPN" hint is correct.
    """
    return (
        "CERTIFICATE_VERIFY_FAILED" in message
        or "[SSL:" in message
        or "SSL certificate problem" in message
        or "unable to get local issuer certificate" in message
        or "self-signed certificate" in message
    )


def has_ssl_trust_failure(results: Iterable["CheckResult"]) -> bool:
    """True iff any non-OK result in ``results`` looks like an SSL trust error."""
    return any(
        r.severity != "ok" and is_ssl_trust_failure(r.message)
        for r in results
    )


# ---- box-python-sdk-gen-specific checks --------------------------------


import sys
from pathlib import Path

from . import config as cfg


def check_python() -> list[CheckResult]:
    """Python interpreter on PATH and meets the minimum version."""
    cur = sys.version_info
    detail = f"Python {cur.major}.{cur.minor}.{cur.micro}"
    if (cur.major, cur.minor) < cfg.MIN_PYTHON:
        need = ".".join(str(x) for x in cfg.MIN_PYTHON)
        return [
            CheckResult(
                "python",
                "fail",
                f"{detail} found; SDK requires {need}+",
                fix_hint=(
                    f"install Python {need}+ from https://www.python.org/downloads/, "
                    "then re-run from a shell using that interpreter."
                ),
            )
        ]
    return [CheckResult("python", "ok", detail)]


def check_pip() -> list[CheckResult]:
    """``pip`` is available via the active interpreter (``python -m pip``).

    We check ``python -m pip`` rather than a bare ``pip`` binary because
    pip is reliably bundled with the Python that's running this code,
    while ``pip`` on PATH varies by install method (homebrew, pyenv,
    system Python, virtualenv, etc.).
    """
    rc, out, err = _run([sys.executable, "-m", "pip", "--version"], timeout=10)
    if rc != 0:
        return [
            CheckResult(
                "pip",
                "fail",
                f"`{sys.executable} -m pip --version` exited {rc}: {(err or out).strip()[:200]}",
                fix_hint=(
                    "ensure pip is installed: `python3 -m ensurepip --upgrade` "
                    "or reinstall Python from python.org."
                ),
            )
        ]
    return [CheckResult("pip", "ok", out.strip().splitlines()[0])]


def check_sdk_importable() -> list[CheckResult]:
    """``box_sdk_gen`` resolves on the current sys.path.

    A WARN (not FAIL) when missing — the wizard's preflight step offers
    to run ``pip install -e .[test,dev]`` to fix it. The user can also
    skip and install manually.
    """
    try:
        import box_sdk_gen  # noqa: F401
    except ImportError as exc:
        return [
            CheckResult(
                "box_sdk_gen",
                "warn",
                f"not importable: {exc}",
                fix_hint=(
                    "from the repo root, run `python3 -m pip install -e .[test,dev]` "
                    "(or pick the dependency-install option in `./scripts/setup`)."
                ),
            )
        ]
    return [
        CheckResult(
            "box_sdk_gen",
            "ok",
            f"importable from {Path(box_sdk_gen.__file__).parent}",
        )
    ]


def check_box_env() -> list[CheckResult]:
    """``.env`` exists at the repo root and declares an auth mode."""
    if not cfg.BOX_ENV_FILE.exists():
        return [
            CheckResult(
                "box-env",
                "warn",
                f"{cfg.BOX_ENV_FILE.name} not found",
                fix_hint="run `./scripts/setup` and pick the auth-credentials step.",
            )
        ]
    values = cfg.read_dotenv(cfg.BOX_ENV_FILE)
    mode = values.get("BOX_AUTH_MODE", "").strip()
    if not mode:
        return [
            CheckResult(
                "box-env",
                "warn",
                f"{cfg.BOX_ENV_FILE.name} present but `BOX_AUTH_MODE` not set",
                fix_hint="re-run `./scripts/setup` and pick the auth-credentials step.",
            )
        ]
    if mode not in cfg.ALL_AUTH_MODES:
        return [
            CheckResult(
                "box-env",
                "fail",
                f"unknown auth mode `{mode}` (expected one of {cfg.ALL_AUTH_MODES})",
                fix_hint="re-run `./scripts/setup` to pick a supported mode.",
            )
        ]
    return [
        CheckResult(
            "box-env",
            "ok",
            f"auth mode = {mode}",
        )
    ]


def check_developer_token() -> list[CheckResult]:
    """When mode=developer_token, the token is set in .env.

    No-op for other modes (returns OK so the doctor stays quiet).
    Developer tokens have a 60-min TTL — freshness, not just presence,
    matters, but we can't detect expiry without a network call.
    """
    if not cfg.BOX_ENV_FILE.exists():
        return [CheckResult("developer-token", "ok", "n/a (no .env yet)")]
    values = cfg.read_dotenv(cfg.BOX_ENV_FILE)
    if values.get("BOX_AUTH_MODE", "").strip() != cfg.AUTH_MODE_DEV_TOKEN:
        return [CheckResult("developer-token", "ok", "n/a (other auth mode)")]
    token = values.get("BOX_DEVELOPER_TOKEN", "").strip()
    if not token:
        return [
            CheckResult(
                "developer-token",
                "fail",
                "mode=developer_token but `BOX_DEVELOPER_TOKEN` is empty",
                fix_hint=(
                    "re-run `./scripts/setup` and pick auth-credentials. Mint "
                    f"a fresh token at {cfg.DEV_CONSOLE_URL}."
                ),
            )
        ]
    return [
        CheckResult(
            "developer-token",
            "ok",
            f"token set ({len(token)} chars). Note: tokens expire after 60 min.",
        )
    ]


def check_jwt_config() -> list[CheckResult]:
    """When mode=jwt, the JWT config JSON exists and parses."""
    if not cfg.BOX_ENV_FILE.exists():
        return [CheckResult("jwt-config", "ok", "n/a (no .env yet)")]
    values = cfg.read_dotenv(cfg.BOX_ENV_FILE)
    if values.get("BOX_AUTH_MODE", "").strip() != cfg.AUTH_MODE_JWT:
        return [CheckResult("jwt-config", "ok", "n/a (other auth mode)")]
    path_str = values.get("BOX_JWT_CONFIG_PATH", "").strip()
    if not path_str:
        return [
            CheckResult(
                "jwt-config",
                "fail",
                "mode=jwt but `BOX_JWT_CONFIG_PATH` not set",
                fix_hint="re-run `./scripts/setup` and pick auth-credentials.",
            )
        ]
    p = Path(path_str).expanduser()
    if not p.exists():
        return [
            CheckResult(
                "jwt-config",
                "fail",
                f"JWT config not at {p}",
                fix_hint=(
                    "verify the path; the developer console downloads it as "
                    "config.json and you can place it anywhere."
                ),
            )
        ]
    import json

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [
            CheckResult(
                "jwt-config",
                "fail",
                f"JWT config at {p} is not valid JSON: {exc}",
                fix_hint="re-download the JWT app config from the developer console.",
            )
        ]
    expected_keys = {"boxAppSettings", "enterpriseID"}
    missing = expected_keys - set(data.keys())
    if missing:
        return [
            CheckResult(
                "jwt-config",
                "warn",
                f"JWT config at {p} missing keys: {sorted(missing)}",
                fix_hint="re-download the JWT app config from the developer console.",
            )
        ]
    return [CheckResult("jwt-config", "ok", f"valid JWT config at {p}")]
