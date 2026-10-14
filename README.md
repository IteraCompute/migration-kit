# IteraCompute Migration Kit

Install dependencies → configure your IteraCompute key → call free Qwen → see a non-empty reply.

Use the official OpenAI SDK with an explicit IteraCompute key, base URL and exact API model ID:

| Setting | Value |
| --- | --- |
| Base URL | `https://api.iteracompute.com/v1` |
| Key variable | `ITERACOMPUTE_API_KEY` |
| Free model ID | `qwen/qwen3.8-27b` |
| Endpoint | Chat Completions |

API model IDs must match the public [Models endpoint](https://api.iteracompute.com/v1/models). **Do not add `iteracompute/` to an API model ID.** These examples explicitly pass `ITERACOMPUTE_API_KEY`; an existing `OPENAI_API_KEY` is never used as a fallback. The free Qwen example disables thinking to get a short visible reply; that option is specific to this model.

## 1. Install dependencies

Clone this repository first:

```sh
git clone https://github.com/IteraCompute/migration-kit.git
cd migration-kit
```

Choose Python (3.10+) or TypeScript (Node.js 22+, npm).

Python, macOS / Linux / WSL:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Python, Windows PowerShell (activation is not required):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

TypeScript, any platform:

```sh
npm ci
```

## 2. Configure your IteraCompute key

[Create an account](https://platform.iteracompute.com/sign-up), verify your email or sign in with Google, then [create an API key](https://platform.iteracompute.com/api-keys) that permits `qwen/qwen3.8-27b`. Free access does not require a card or recharge. Save the secret shown once.

Set the variable in the **same terminal** you will use to run the example. Replace `your-api-key` with your IteraCompute key.

Bash / zsh / WSL:

```sh
export ITERACOMPUTE_API_KEY="your-api-key"
```

Windows PowerShell:

```powershell
$env:ITERACOMPUTE_API_KEY = "your-api-key"
```

Keep the key on the server or in your local terminal. Do not commit it, paste it into issues, or put it in browser code. `.env` files are ignored but are **not automatically loaded** by these examples.

## 3. Call free Qwen

Python, macOS / Linux / WSL:

```sh
python examples/openai_python.py
```

Python, Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe examples/openai_python.py
```

TypeScript, any platform:

```sh
npm run quickstart
```

## 4. Check the reply

Expected stdout (npm also prints its script banner):

```text
Hello!
```

Wording may vary. Success requires a non-empty `choices[0].message.content` and exit code 0. Missing keys, API errors and empty replies exit with code 1. Registration or HTTP 200 alone does not complete this check. Requests have a 180-second timeout and no automatic retries; free capacity may queue.

## Two complete examples

| Example | What you will run and verify |
| --- | --- |
| [Text summarizer](examples/summarizer/) | Read a bundled meeting document, print its summary, and save a non-empty UTF-8 output file. |
| [OpenCode coding tool](examples/opencode/) | Connect free Qwen, repair a failing slugify function in a disposable project, and run four tests. |

See [acceptance results](docs/acceptance.md) for the exact versions, commands, outputs and validation scope. Each example has its own complete setup and troubleshooting instructions.

## Common errors

| Symptom | Fix |
| --- | --- |
| `Set ITERACOMPUTE_API_KEY` | Set an actual IteraCompute key in this terminal; a placeholder, blank value or only `OPENAI_API_KEY` is insufficient. |
| `ModuleNotFoundError: openai` / `tsx` not found | Install dependencies from the repository root; use the same Python interpreter / virtual environment that ran pip. For TypeScript run `npm ci`. |
| HTTP 401 | The IteraCompute key is missing, invalid or revoked. Replace it; do not use an OpenAI key. |
| HTTP 403 | Check that the key permits `qwen/qwen3.8-27b`. Free Qwen does not require paid balance. |
| HTTP 404 | Keep `/v1` in the base URL and use `qwen/qwen3.8-27b` exactly, without an `iteracompute/` prefix. Use Chat Completions. |
| HTTP 400 | Check request options and reduce the input/output budget. Free context includes input plus requested maximum output. |
| HTTP 429 | Check monthly allowance and TPM in the Console. Honor `Retry-After`; avoid parallel retries. See [free limits](https://iteracompute.com/free/). |
| Empty model reply | The sample fails even on HTTP 200. Use the supplied short prompt and Qwen thinking setting, then retry when capacity is available. |
| Network / timeout / HTTP 5xx | Check connectivity and provider status; retry a single request after a delay. Do not disable TLS verification. |

Other models can require paid balance; `qwen/qwen3.8-2.4t-a95b` is a different model. Check [current pricing](https://iteracompute.com/pricing/) and [API documentation](https://iteracompute.com/docs.html) before switching.

## Development checks

After installing both sets of dependencies:

```sh
python -m unittest discover -s tests -v
```

On Windows use `.\.venv\Scripts\python.exe` instead of `python`. These offline tests verify the actual SDK request body, IteraCompute authentication, missing keys, empty replies, HTTP errors and summary file writes. They use fake credentials and do not establish live API acceptance.

[API docs](https://iteracompute.com/docs.html) · [Integrations](https://iteracompute.com/integrations/) · [Pricing CLI](https://github.com/IteraCompute/pricing)
