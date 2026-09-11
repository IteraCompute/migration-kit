"""Migrate your OpenAI code to IteraCompute: two-line change."""
from openai import OpenAI

# 1) base_url
client = OpenAI(base_url="https://api.iteracompute.com/v1")

# 2) model id
resp = client.chat.completions.create(
    model="z-ai/glm-5.3-flash",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(resp.choices[0].message.content)

# Streaming works too:
for chunk in client.chat.completions.create(
    model="z-ai/glm-5.3-flash",
    messages=[{"role": "user", "content": "Count to 5"}],
    stream=True,
):
    print(chunk.choices[0].delta.content or "", end="")
