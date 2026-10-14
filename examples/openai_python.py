"""First free Qwen call. Run from the repository root after installing requirements."""
import os
import sys

from openai import APIConnectionError, APIStatusError, OpenAI


def main():
    key = os.environ.get("ITERACOMPUTE_API_KEY", "").strip()
    if not key or key == "your-api-key":
        raise ValueError("Set ITERACOMPUTE_API_KEY to your IteraCompute key; see README.md.")
    client = OpenAI(
        base_url="https://api.iteracompute.com/v1",
        api_key=key,
        timeout=180,
        max_retries=0,
    )
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": "Reply with exactly: Hello!"}],
        max_tokens=512,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    text = response.choices[0].message.content if response.choices else None
    if not text or not text.strip():
        raise ValueError("Empty model reply: activation is incomplete; see README.md troubleshooting.")
    print(text.strip())


if __name__ == "__main__":
    try:
        main()
    except APIStatusError as error:
        sys.exit(f"IteraCompute HTTP {error.status_code}; see README.md troubleshooting.")
    except APIConnectionError:
        sys.exit("Cannot reach IteraCompute (network or timeout); see README.md troubleshooting.")
    except ValueError as error:
        sys.exit(str(error))
