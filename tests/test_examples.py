"""Offline checks for authentication, visible replies and summary file writes."""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx2 as httpx
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


QUICKSTART = load("quickstart", "examples/openai_python.py")
SUMMARY = load("summary", "examples/summarizer/summarize.py")


class PythonExamples(unittest.TestCase):
    def client(self, content="Hello!", choices=True):
        def respond(request):
            self.assertEqual(str(request.url), "https://api.iteracompute.com/v1/chat/completions")
            self.assertEqual(request.headers["authorization"], "Bearer itera-test")
            body = json.loads(request.content)
            self.assertEqual(body["model"], "qwen/qwen3.8-27b")
            self.assertEqual(body["chat_template_kwargs"], {"enable_thinking": False})
            return httpx.Response(200, json={
                "id": "test", "object": "chat.completion", "created": 0,
                "model": body["model"],
                "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": content}}] if choices else [],
            })
        return OpenAI(api_key="itera-test", base_url="https://api.iteracompute.com/v1",
                      http_client=httpx.Client(transport=httpx.MockTransport(respond)))

    def test_missing_key_does_not_fall_back_to_openai(self):
        for value in ["", " ", "your-api-key"]:
            with self.subTest(value=value), patch.dict(os.environ, {"ITERACOMPUTE_API_KEY": value, "OPENAI_API_KEY": "wrong-provider"}), patch.object(QUICKSTART, "OpenAI") as factory:
                with self.assertRaisesRegex(ValueError, "ITERACOMPUTE_API_KEY"):
                    QUICKSTART.main()
                factory.assert_not_called()

    def test_request_uses_itera_key_and_exact_model(self):
        with patch.dict(os.environ, {"ITERACOMPUTE_API_KEY": "itera-test", "OPENAI_API_KEY": "wrong-provider"}), patch.object(QUICKSTART, "OpenAI", return_value=self.client()) as factory, contextlib.redirect_stdout(io.StringIO()) as output:
            QUICKSTART.main()
            self.assertEqual(factory.call_args.kwargs["api_key"], "itera-test")
            self.assertEqual(output.getvalue().strip(), "Hello!")

    def test_empty_replies_fail(self):
        for text, choices in [(None, True), ("  ", True), ("Hello", False)]:
            with self.subTest(text=text, choices=choices), patch.dict(os.environ, {"ITERACOMPUTE_API_KEY": "itera-test"}), patch.object(QUICKSTART, "OpenAI", return_value=self.client(text, choices)):
                with self.assertRaisesRegex(ValueError, "Empty model reply"):
                    QUICKSTART.main()

    def test_summary_output_and_invalid_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp) / "source.txt", Path(tmp) / "summary.txt"
            source.write_text("Meeting notes", encoding="utf-8")
            argv = ["summarize.py", str(source), "--output", str(target)]
            with patch.object(sys, "argv", argv), patch.dict(os.environ, {"ITERACOMPUTE_API_KEY": "itera-test"}), patch.object(SUMMARY, "OpenAI", return_value=self.client("- Summary")), contextlib.redirect_stdout(io.StringIO()):
                SUMMARY.main()
            self.assertEqual(target.read_text(encoding="utf-8"), "- Summary\n")
            target.unlink()
            for text in [None, " "]:
                with patch.object(sys, "argv", argv), patch.dict(os.environ, {"ITERACOMPUTE_API_KEY": "itera-test"}), patch.object(SUMMARY, "OpenAI", return_value=self.client(text)):
                    with self.assertRaisesRegex(ValueError, "Empty model reply"):
                        SUMMARY.main()
                self.assertFalse(target.exists())
            source.write_text("  ", encoding="utf-8")
            with patch.object(sys, "argv", argv), patch.object(SUMMARY, "OpenAI") as factory:
                with self.assertRaisesRegex(ValueError, "Input file is empty"):
                    SUMMARY.main()
                factory.assert_not_called()


class TypeScriptExamples(unittest.TestCase):
    def run_example(self, key, mode="success"):
        env = dict(os.environ, ITERACOMPUTE_API_KEY=key, OPENAI_API_KEY="wrong-provider", MOCK_MODE=mode)
        return subprocess.run(["node", "--import", "tsx", "--import", "./tests/mock-fetch.mjs", "examples/openai_typescript.ts"], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)

    def test_missing_key_does_not_fall_back_to_openai(self):
        for key in ["", " ", "your-api-key"]:
            result = self.run_example(key)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ITERACOMPUTE_API_KEY", result.stderr)

    def test_request_and_visible_reply(self):
        result = self.run_example("itera-test")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "Hello!")

    def test_empty_reply_and_http_errors_fail(self):
        for mode, message in [("empty", "Empty model reply"), ("no-choices", "Empty model reply"), ("401", "HTTP 401"), ("429", "HTTP 429")]:
            result = self.run_example("itera-test", mode)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(message, result.stderr)


if __name__ == "__main__":
    unittest.main()
