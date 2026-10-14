# Acceptance results

Live acceptance is pending a restricted IteraCompute test key. Offline checks and live API runs are recorded separately. No earlier Hello-only coding test is presented as proof of code edits or command execution.

## Python and TypeScript quickstarts

Pending live run: a non-empty visible reply and exit code 0 for each SDK.

## Summarizer

Pending live run: three summary bullets, exit code 0, non-empty saved file and source-fact review.

## OpenCode

Pending live run: starter baseline 1 pass / 3 fail, actual tool-driven file change, unchanged test file, independent rerun 4 pass / 0 fail, and non-empty final reply.

## Offline checks

Run `python -m unittest discover -s tests -v` after installing Python and TypeScript dependencies. These use fake credentials and mocked HTTP transport and do not verify model availability.
