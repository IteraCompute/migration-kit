# IteraCompute Migration Kit

Migrate from OpenAI to IteraCompute in one line. No new SDK, no protocol change — just a new `base_url` and model ID.

- Base URL: `https://api.iteracompute.com/v1`
- Model ID format: `iteracompute/<model>` (or `<org>/<model>`, e.g. `z-ai/glm-5.3-flash`)
- Protocol: OpenAI API / SSE streaming. No lock-in.

## Examples

- Python (official `openai` SDK): [examples/openai_python.py](examples/openai_python.py)
- TypeScript (official `openai` SDK): [examples/openai_typescript.ts](examples/openai_typescript.ts)

## Current lineup (check live: https://api.iteracompute.com/v1/models)

GLM 5.3 Flash · GLM 5.3 · DeepSeek V4 Flash · DeepSeek V4 Pro · Qwen3.8-27B · Qwen3.8 2.4T · Ornith 1.5 35B-A3B · MiniMax M3 · Kimi K3

Pricing tool: [iteracompute-pricing](https://github.com/iteracompute/pricing) (prints a live price table from `/v1/models`).
