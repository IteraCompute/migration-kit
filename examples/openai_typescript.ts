import OpenAI from "openai";

const client = new OpenAI({ baseURL: "https://api.iteracompute.com/v1" });

const resp = await client.chat.completions.create({
  model: "z-ai/glm-5.3-flash",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(resp.choices[0]?.message?.content);
