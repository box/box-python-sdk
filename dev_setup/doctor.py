"""``doctor`` — read-only environment audit.

Calls every registered check function and prints results. Same
``CheckResult`` rendering as the wizard, so the user gets the same
``[OK]`` / ``[WARN]`` / ``[FAIL]`` glyphs from both surfaces.

Exits non-zero only on hard failures. Warnings are tolerated — they
mean "optional thing isn't set up" rather than "your environment is
broken". Tune ``DOCTOR_FAIL_ON_WARN`` per repo if your audience needs
strict exit codes.
"""

from __future__ import annotations

import sys
from collections.abc import Callable

from . import checks
from .checks import CheckResult, DoctorReport
from .prompts import banner, paced_print, print_results

# ---- customize per repo -------------------------------------------------

DOCTOR_TITLE: str = "Box Python SDK doctor"
DOCTOR_TAGLINE: str = (
    "Read-only audit. Re-runs each setup step's check function so you can\n"
    "see what's wired up and what isn't, without rerunning the wizard."
)

# Whether to exit non-zero on warnings. Default False — warnings here
# usually mean "auth mode picked but credential file path doesn't exist
# yet", which is not a hard failure.
DOCTOR_FAIL_ON_WARN: bool = False

CheckFn = Callable[[], list[CheckResult]]
DOCTOR_CHECKS: list[CheckFn] = [
    checks.check_python,
    checks.check_pip,
    checks.check_sdk_importable,
    checks.check_box_env,
    checks.check_developer_token,
    checks.check_jwt_config,
]


# ---- runner -------------------------------------------------------------


def run_all_checks() -> DoctorReport:
    """Call every registered check and assemble a ``DoctorReport``."""
    report = DoctorReport()
    for check in DOCTOR_CHECKS:
        try:
            results = check()
        except Exception as exc:  # noqa: BLE001 - keep the doctor robust
            results = [
                CheckResult(
                    name=check.__name__,
                    severity="fail",
                    message=f"check raised {type(exc).__name__}: {exc}",
                    fix_hint="report this as a doctor bug.",
                )
            ]
        report.add(*results)
    return report


def main(argv: list[str] | None = None) -> int:
    """Entry point. Prints banner, runs all checks, returns exit code."""
    argv = list(argv if argv is not None else sys.argv[1:])

    banner(DOCTOR_TITLE)
    paced_print(DOCTOR_TAGLINE, after_ms=300)
    print()

    report = run_all_checks()
    print_results(report.results, show_ok=True, show_fix=True)

    print()
    fails = sum(1 for r in report.results if r.severity == "fail")
    warns = sum(1 for r in report.results if r.severity == "warn")
    oks = sum(1 for r in report.results if r.severity == "ok")
    paced_print(f"  Summary: {oks} OK, {warns} WARN, {fails} FAIL", after_ms=150)

    if fails > 0:
        return 1
    if DOCTOR_FAIL_ON_WARN and warns > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
