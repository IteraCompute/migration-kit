import assert from "node:assert/strict";

globalThis.fetch = async (input, options) => {
  const request = new Request(input, options);
  assert.equal(request.url, "https://api.iteracompute.com/v1/chat/completions");
  assert.equal(request.headers.get("authorization"), "Bearer itera-test");
  const body = await request.json();
  assert.equal(body.model, "qwen/qwen3.8-27b");
  assert.deepEqual(body.chat_template_kwargs, { enable_thinking: false });
  const mode = process.env.MOCK_MODE;
  if (["401", "429"].includes(mode)) {
    return Response.json({ error: { message: "Test failure", type: "test_error" } }, { status: Number(mode) });
  }
  return Response.json({
    id: "test", object: "chat.completion", created: 0, model: body.model,
    choices: mode === "no-choices" ? [] : [{ index: 0, finish_reason: "stop", message: { role: "assistant", content: mode === "empty" ? "  " : "Hello!" } }],
  });
};
// With a missing IteraCompute key the request must fail before reaching fetch.
