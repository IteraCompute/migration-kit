# Acceptance results

Live acceptance is pending a restricted IteraCompute test key. Offline checks and live API runs are recorded separately. No earlier Hello-only coding test is presented as proof of code edits or command execution.

## Python and TypeScript quickstarts

Pending live run: a non-empty visible reply and exit code 0 for each SDK.

## Summarizer

Pending live run: three summary bullets, exit code 0, non-empty saved file and source-fact review.

## OpenCode

Pending live run: starter baseline 1 pass / 3 fail, actual tool-driven file change, unchanged test file, independent rerun 4 pass / 0 fail, and non-empty final reply.

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

The SDK checks use fake credentials and mocked HTTP transport. The OpenCode listing and starter baseline do not establish successful model access, edits or tool execution. The real acceptance rows above remain pending until a restricted key is available.
