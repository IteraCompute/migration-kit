import OpenAI from "openai";

async function main() {
  const apiKey = process.env.ITERACOMPUTE_API_KEY?.trim();
  if (!apiKey || apiKey === "your-api-key") {
    throw new Error("Set ITERACOMPUTE_API_KEY to your IteraCompute key; see README.md.");
  }
  const client = new OpenAI({
    baseURL: "https://api.iteracompute.com/v1",
    apiKey,
    timeout: 180_000,
    maxRetries: 0,
  });
  const response = await client.chat.completions.create({
    model: "qwen/qwen3.8-27b",
    messages: [{ role: "user", content: "Reply with exactly: Hello!" }],
    max_tokens: 512,
    ...{ chat_template_kwargs: { enable_thinking: false } },
  });
  const text = response.choices[0]?.message?.content?.trim();
  if (!text) {
    throw new Error("Empty model reply: activation is incomplete; see README.md troubleshooting.");
  }
  console.log(text);
}

main().catch((error: unknown) => {
  if (error instanceof OpenAI.APIError) {
    console.error(`IteraCompute HTTP ${error.status ?? "connection error"}; see README.md troubleshooting.`);
  } else {
    console.error(error instanceof Error ? error.message : "Request failed.");
  }
  process.exitCode = 1;
});
