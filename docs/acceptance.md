# Acceptance results

Verified October 14, 2026 against `https://api.iteracompute.com/v1` with `qwen/qwen3.8-27b` and a user-supplied test key. All four examples returned non-empty replies and exited successfully. Tests ran on Windows with Python 3.11.4, Node.js 25.2.1, Python OpenAI 3.30.0, TypeScript OpenAI 7.32.0, tsx 4.23.15 and OpenCode 1.19.0.

[Machine-readable evidence](acceptance-2026-10-14.json) contains actual stdout, coding tool outcomes, code changes and the independent test rerun. Credentials, local machine paths and session IDs are omitted.

## Python and TypeScript quickstarts

Ran the documented Python command and `npm run quickstart` sequentially. Each printed `Hello!` and exited with code 0. TypeScript also printed npm's script banner. Both explicitly passed the IteraCompute key and used the exact API model ID.

```text
Hello!
```

## Summarizer

Ran `examples/summarizer/summarize.py examples/summarizer/meeting.txt --output summary.txt` from the root using the virtual environment. Actual stdout:

```text
• Customer feedback dashboard launch decision: go live on October 21, but the launch is blocked until CSV export tests pass and the support guide is reviewed.
• Maya owns the release checklist and must finish it by October 18; Leo will add CSV export before launch.
• Mobile layout is deferred to the next release.

Saved: summary.txt
```

Exit code 0; the saved file was non-empty and matched the printed summary. Reviewed all three bullets against the source: launch date, owners, checklist deadline, CSV export, deferred mobile work and blockers were preserved. Wording will vary on another run.

## OpenCode

Installed OpenCode from the included lockfile, copied the starter and configuration into `workspace`, and ran the documented Build-agent command.

| Check | Actual result |
| --- | --- |
| Starter before repair | 4 tests, 1 pass, 3 fail; exit code 1. |
| Model tool execution | Read the function and tests, wrote the repaired function, then ran `node --test slugify.test.mjs` successfully. |
| Test integrity | `slugify.test.mjs` remained byte-for-byte identical to the starter. Its SHA-256 is in the evidence file. |
| Agent completion | Non-empty final reply reported all four tests passing. |
| Independent rerun | 4 tests, 4 pass, 0 fail; exit code 0. |

Actual model-written function:

```js
export function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
```

The configuration explicitly sets free Qwen's prices to zero; the final run's OpenCode cost estimate was zero. Client estimates are not billing evidence; check allowance and charges in the IteraCompute Console.

This verifies a real code-edit and test workflow on Windows. macOS/Linux, larger repositories, hosted deployments and browser applications were not tested.

## Offline checks

Verified October 14, 2026 on Windows with Python 3.11.4 and Node.js 25.2.1:

| Check | Actual result |
| --- | --- |
| Python dependency install | `openai==3.30.0` installed in a fresh virtual environment. |
| TypeScript dependency install | `openai@7.32.0`, `tsx@4.23.15` installed from the package manifest; lockfile included. |
| `python -m unittest discover -s tests -v` | 7 tests passed, including missing/blank/placeholder keys, explicit IteraCompute authentication, exact API model ID, empty replies, HTTP 401/429 and summary file writes. |
| `npm run code -- --version` in `examples/opencode` | `1.19.0` |
| `npm run code -- models iteracompute` with a fake key | The configured `iteracompute/qwen/qwen3.8-27b` selector was recognized. No chat request was made. |
| `node --test slugify.test.mjs` in a fresh starter workspace | 4 tests, 1 pass, 3 fail, exit code 1. This reproduces the coding task before a model repairs it. |

These offline SDK checks use fake credentials and mocked HTTP transport. They complement the real API and coding workflow results above.
