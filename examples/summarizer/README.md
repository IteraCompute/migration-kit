# Text summarizer with free Qwen

This server-side Python CLI reads a UTF-8 text file, calls `qwen/qwen3.8-27b`, prints three summary bullets and saves them to `summary.txt`. Only non-empty replies are written. No web server or database is needed.

## Install and configure

From the repository root, use Python 3.10+:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export ITERACOMPUTE_API_KEY="your-api-key"
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:ITERACOMPUTE_API_KEY = "your-api-key"
```

Get the key from [IteraCompute API Keys](https://platform.iteracompute.com/api-keys) and permit `qwen/qwen3.8-27b`. Run the [first free call](../../README.md) before this example.

## Run

From the repository root:

```sh
python examples/summarizer/summarize.py examples/summarizer/meeting.txt --output summary.txt
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe examples/summarizer/summarize.py examples/summarizer/meeting.txt --output summary.txt
Get-Content summary.txt
```

On Bash read the saved file with `cat summary.txt`. For your own input, replace `examples/summarizer/meeting.txt` with the path to a small UTF-8 document. Input plus requested output must fit your free context limit; large documents need splitting before use.

## Expected result and acceptance

The output should contain three non-empty bullets covering the October 21 launch, Maya's October 18 checklist, Leo's CSV export, the deferred mobile layout and launch blockers. It ends with `Saved: summary.txt`. Wording is nondeterministic.

Check exit code 0, a non-empty `summary.txt`, and the source facts. A file created without an API reply is not success. See [the actual acceptance record](../../docs/acceptance.md#summarizer).

## Troubleshooting

- Missing file / invalid UTF-8: check the input path and save the document as UTF-8.
- `Input file is empty`: provide actual text; no API call is sent for blank input.
- Empty API reply: the command fails and does not create or replace the output file.
- Output path error: choose a writable path with an existing parent directory.
- HTTP 401/403/404/429 or timeout: use the [shared troubleshooting table](../../README.md#common-errors).

[Website SDK guide](https://iteracompute.com/integrations/openai-sdk/) · [API docs](https://iteracompute.com/docs.html)
