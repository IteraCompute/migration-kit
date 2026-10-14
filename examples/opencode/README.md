# OpenCode + free Qwen: repair code and run tests

Use OpenCode's Build agent with IteraCompute Chat Completions to repair a small JavaScript function. The bundled starter has one passing and three failing tests. Acceptance requires an actual file edit, four passing tests, and a non-empty completed reply.

## 1. Install

Use Node.js 22+ and npm. From the migration-kit root:

```sh
cd examples/opencode
npm ci
npm run code -- --version
```

The tool version is fixed by the lockfile. [OpenCode CLI](https://opencode.ai/docs/cli/) and [custom provider documentation](https://opencode.ai/docs/providers/#custom-provider) describe the configuration.

## 2. Configure your IteraCompute key

Create a key at [API Keys](https://platform.iteracompute.com/api-keys) permitting `qwen/qwen3.8-27b`. In this terminal:

```sh
export ITERACOMPUTE_API_KEY="your-api-key"
```

PowerShell:

```powershell
$env:ITERACOMPUTE_API_KEY = "your-api-key"
```

`opencode.json` reads that variable explicitly through `{env:ITERACOMPUTE_API_KEY}`. Both primary and small model use free Qwen; only the IteraCompute provider is enabled. The key is never stored in the configuration file.

**Model ID distinction:** OpenCode's `model` selector is `iteracompute/qwen/qwen3.8-27b`: `iteracompute` selects the configured client provider. The model key inside `provider.iteracompute.models`, and the model ID sent to the API, are `qwen/qwen3.8-27b`. Never copy OpenCode's full selector into the API `model` field.

## 3. Make a disposable project and reproduce the bug

From `examples/opencode`, Bash:

```sh
mkdir workspace
cp opencode.json starter/slugify.mjs starter/slugify.test.mjs workspace/
cd workspace
node --test slugify.test.mjs
```

PowerShell:

```powershell
New-Item -ItemType Directory workspace
Copy-Item opencode.json, starter/slugify.mjs, starter/slugify.test.mjs workspace/
Set-Location workspace
node --test slugify.test.mjs
```

Expected baseline: **1 pass, 3 fail**, exit code 1. For a fresh run use a new workspace or replace only `workspace/slugify.mjs` with the bundled starter. Keep the starter and test expectations unchanged.

## 4. Ask OpenCode to fix it

From `workspace` (npm runs scripts from its package directory; `--dir workspace` selects the disposable project):

```sh
npm --prefix .. run code -- run --dir workspace --agent build --format json "Fix slugify.mjs so all four existing tests pass. Lowercase ASCII letters, preserve digits, replace runs of other characters with one hyphen, and trim leading/trailing hyphens. Do not change slugify.test.mjs. Run node --test slugify.test.mjs and report the result."
```

This same command works in PowerShell. The example permits reading and editing files plus `node --test`; other tools and shell commands are denied. Use this only inside the disposable project. JSON events should include an edit, a test execution, and a final text reply.

## 5. Verify independently

```sh
node --test slugify.test.mjs
```

Expected: **4 tests, 4 pass, 0 fail**, exit code 0, with a changed `slugify.mjs` and unchanged tests. The agent should provide a non-empty final reply describing the test result. See [actual acceptance results](../../docs/acceptance.md#opencode).

## Common errors

| Symptom | Fix |
| --- | --- |
| Key / 401 / 403 | Set the actual `ITERACOMPUTE_API_KEY` in the process environment and check free Qwen permission. `OPENAI_API_KEY` is not used here. |
| Model not found / 404 | Check the selector versus API ID distinction above and keep `/v1` in `baseURL`. |
| Tool denied / unfinished task | Use Build mode in `workspace`, with its copied `opencode.json`. Inspect the JSON events; only file operations and `node --test` are enabled. |
| Tests still fail / tests were changed | Restore the original tests from `starter`, inspect the function diff, and retry the small task. A chat reply alone is insufficient. |
| 429 / timeout / empty reply | Check allowance and TPM, honor `Retry-After`, and run the [first free call](../../README.md) separately. Do not start repeated parallel tasks. |

[Website OpenCode guide](https://iteracompute.com/integrations/opencode/) · [API docs](https://iteracompute.com/docs.html)
