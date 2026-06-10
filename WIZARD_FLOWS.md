# Box Python SDK (v10) — Setup Wizard Quick Reference

A visual reference for the optional setup wizard added by the
`./scripts/setup` script. The wizard is **opt-in** — the SDK works
fine without it; this just streamlines first-time onboarding.

---

## At a glance

| Command                                | What it does                                                              |
| -------------------------------------- | ------------------------------------------------------------------------- |
| `./scripts/setup`                      | First-run + repair wizard. Picker-driven, idempotent.                     |
| `./scripts/doctor`                     | Read-only audit. Re-runs each step's check function and prints results.   |
| `./scripts/setup` then `recommended`   | Verify Python + pip + SDK importable, capture auth credentials, print a smoke snippet. |
| `WIZARD_PACE_MS=0 ./scripts/setup`     | Disable pacing for CI / scripted onboarding.                              |
| `WIZARD_PACE_MS=400 ./scripts/setup`   | Slow pacing for first-time users who want extra read time.                |

The wizard never modifies SDK source files. It writes one file at the
repo root: **`.env`** (gitignored). The Python package is named
`dev_setup/` (not `setup/`) to avoid colliding with `setup.py` and
`setuptools.find_packages()`.

---

## Decision tree

```mermaid
flowchart TD
    Start([./scripts/setup]) --> Banner[Print banner +<br/>3-step picker]
    Banner --> Picker{Picker}
    Picker -->|recommended<br/>or `all`| AllSet[Run steps 1, 2, 3]
    Picker -->|1| OnlyPre[Step 1 only]
    Picker -->|2| OnlyAuth[Step 2 only]
    Picker -->|3| OnlySmoke[Step 3 only]
    Picker -->|none| Exit([Exit cleanly])

    AllSet --> S1[Step 1<br/>Python + dependencies preflight]
    OnlyPre --> S1
    S1 --> PythonCheck{Python >= 3.8<br/>and pip works?}
    PythonCheck -->|no| FailHint[Print install hint, abort step]
    PythonCheck -->|yes| ImportCheck{box_sdk_gen<br/>importable?}
    ImportCheck -->|yes| S2[Step 2<br/>Auth credentials]
    ImportCheck -->|no| OfferInstall{Run pip install -e .[test,dev]?}
    OfferInstall -->|yes| PipInstall[pip install with progress watchdog]
    OfferInstall -->|no| S2
    PipInstall --> S2

    OnlyAuth --> S2
    S2 --> ModePicker{Auth mode?}
    ModePicker -->|1| DevToken[Mint Developer Token<br/>at app.box.com/developers/console<br/>capture via getpass]
    ModePicker -->|2| JWT[Capture JWT config.json<br/>path]
    ModePicker -->|3| CCG[Capture client ID/secret/<br/>EID-or-UID]
    ModePicker -->|4| OAuth[Capture client ID/secret/<br/>redirect URI]

    DevToken --> WriteEnv[Write .env]
    JWT --> WriteEnv
    CCG --> WriteEnv
    OAuth --> WriteEnv

    WriteEnv --> S3[Step 3<br/>Smoke test snippet]
    OnlySmoke --> S3
    S3 --> SnippetCheck{.env exists?}
    SnippetCheck -->|yes| PrintSnippet[Print Python snippet<br/>keyed to chosen mode]
    SnippetCheck -->|no| HintGoBack[Hint: pick step 2 first]

    PrintSnippet --> Footer[Print completion footer +<br/>doctor + docs links]
    HintGoBack --> Footer
    Footer --> Done([User runs ./scripts/doctor<br/>to verify])
```

---

## Steps

| # | Step                              | Recommended | Check                                                              | Repair                                                                     | Writes                       |
| - | --------------------------------- | ----------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------- | ---------------------------- |
| 1 | Python + dependencies preflight   | yes         | `python >= 3.8`, `python -m pip --version`, `import box_sdk_gen`   | offer `pip install -e .[test,dev]` (progress watchdog while it runs)       | nothing (modifies site-packages via pip) |
| 2 | Auth credentials                  | yes         | `.env` exists with `BOX_AUTH_MODE` set                             | inner picker for Developer Token / JWT / CCG / OAuth, then capture creds   | `.env`                       |
| 3 | Smoke test snippet                | yes         | (none — printing-only step)                                        | print a copy-pasteable Python program keyed to the chosen auth mode        | nothing                      |

---

## Picker grammar

| Input         | Means                                            |
| ------------- | ------------------------------------------------ |
| `1,2,3`       | comma-separated indices                          |
| `1-3`         | a range (inclusive)                              |
| `all`         | every step                                       |
| `recommended` | every `[R]` step (the default if you press Enter) |
| `none`        | exit without running anything                    |

---

## Auth modes

| Mode                    | When to pick                                | What the wizard collects                                  | Where it lands in `.env`                  |
| ----------------------- | ------------------------------------------- | --------------------------------------------------------- | ----------------------------------------- |
| Developer Token         | Local dev, testing on your own account      | One token (60-min TTL)                                    | `BOX_DEVELOPER_TOKEN`                      |
| JWT                     | Server-to-server, no user impersonation     | Path to JWT config JSON                                   | `BOX_JWT_CONFIG_PATH`                      |
| Client Credentials (CCG) | Server-to-server, modern flow              | Client ID, secret, enterprise OR user ID                  | `BOX_CCG_*`                                |
| OAuth 2.0               | Multi-user, end-user-facing app             | Client ID, secret, redirect URI                           | `BOX_OAUTH_*`                              |

The wizard always sets `BOX_AUTH_MODE` to one of `developer_token`,
`jwt`, `ccg`, or `oauth`. The doctor reads it to decide which
mode-specific check function should run.

---

## Cross-cutting features

### Pacing
Output is paced so multi-paragraph blocks become readable. Override
with `WIZARD_PACE_MS=<ms>` (`0` disables, `80` is default, `400` is a
slow ramp). Pacing auto-disables when stdout isn't a TTY.

### Self-contained credential capture
The wizard reads `.env` itself when needed and never asks you to
"first source X" or "first export Y". Cloning the repo and running
`./scripts/setup` is the only prerequisite.

### Doctor-symmetric checks
Every wizard step has a check function in `dev_setup/checks.py` that
the doctor calls. Re-running `./scripts/doctor` after a wizard run
prints all results in one shot, no prompts, exit code 0 when
everything's OK.

### Hidden secret entry
Tokens, client secrets, etc. are read with `getpass.getpass` so they
never echo to the terminal or land in shell history.

### Owner-only secrets file
`.env` is chmod 0600 on POSIX systems. Best-effort on Windows /
unusual filesystems.

### Progress watchdog
Long-running subprocesses (>5s) print `current action: <description>`
so they don't look hung. Step 1's `pip install` run uses this; you'll
see something like `current action: installing SDK in editable mode
(pip)` after a few seconds, then `→ done in 47s` when complete.

---

## Common recovery paths

| Symptom                                              | What to try                                                                       |
| ---------------------------------------------------- | --------------------------------------------------------------------------------- |
| `[FAIL] python: ... < 3.8`                           | Install Python 3.8+ from python.org, then re-run from a shell using that interpreter. |
| `[FAIL] pip: ...`                                    | `python3 -m ensurepip --upgrade`, or reinstall Python.                            |
| `[WARN] box_sdk_gen: not importable`                 | `./scripts/setup` and accept the pip-install prompt.                              |
| `[WARN] box-env: not found`                          | `./scripts/setup` and pick step 2.                                                |
| `[FAIL] developer-token: empty`                      | Mint a fresh one at https://app.box.com/developers/console, re-run step 2.        |
| `[FAIL] jwt-config: not at <path>`                   | Verify the path; the developer console downloads as `config.json`.               |
| Picker rejected my input                             | Use commas, ranges, `all`, `recommended`, or `none`. No spaces inside numbers.    |
| Smoke snippet 401's when run                         | Token expired (Developer Tokens last 60 min). Re-run step 2 for a fresh one.      |

---

## Verifying success

```bash
./scripts/doctor                                  # Should report all OK.
pytest                                            # Run the SDK's own tests
```

For a real end-to-end check, paste the snippet from the wizard's step 3
into a `.py` file with `box-sdk-gen` on `sys.path` (use
`pip install -e .` from the repo root), run it, and confirm it prints
your name.

---

## What this wizard does NOT do

- **Run the OAuth callback flow**: OAuth needs an HTTP server to
  receive the redirect, which is application-specific. The wizard
  captures credentials; running the flow is on you.
- **Refresh tokens**: Developer Tokens expire after 60 minutes. The
  doctor reminds you of that but doesn't auto-refresh.
- **Manage virtualenvs**: it uses whichever Python runs the wizard.
  Activate your venv before running `./scripts/setup`.
- **Manage multiple environments**: one repo = one `.env`. If you need
  profiles, layer that on top.

---

Built using
[`setup-wizard-squared`](https://github.com/NatalieNobile/setup-wizard-squared).
See its `reference/patterns.md` for the seven design principles that
shape this wizard.
