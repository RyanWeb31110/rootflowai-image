---
name: rootflowai-image-count
description: Generate or edit images through the RootFlowAI-compatible images API using the count-billed lane. Use this skill when the user wants the `gpt-image-2-count` model, the count API key, or a separate per-request billing workflow.
---

# RootFlowAI Image Count

## Overview

Use this skill for the count-billed RootFlowAI image workflow.
It should prefer the `gpt-image-2-count` model and the count credential profile unless the user explicitly asks for something else.

## Quick Start

1. Use `ROOTFLOWAI_COUNT_API_KEY` for authentication.
2. Use `generate_image.py` for prompt-to-image work.
3. Use `edit_image.py` for image editing work.
4. Pass `--profile count` so the billing route stays explicit.
5. Prefer `gpt-image-2-count` as the model.

Example:

```bash
ROOTFLOWAI_COUNT_API_KEY=your_count_key_here \
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-count \
  --prompt "Three oath brothers doing a short-video livestream" \
  --output-dir ./out
```

```bash
ROOTFLOWAI_COUNT_API_KEY=your_count_key_here \
python3 ../../scripts/edit_image.py \
  --profile count \
  --model gpt-image-2-count \
  --image /absolute/path/to/portrait.jpg \
  --prompt "Convert this portrait into an American-style professional headshot" \
  --output-dir ./out
```

## Defaults

- generation endpoint: `https://api.rootflowai.com/v1/images/generations`
- edit endpoint: `https://api.rootflowai.com/v1/images/edits`
- profile: `count`
- model: `gpt-image-2-count`
- size: `1536x1024`
- quality: `high`

## Workflow

- In the source repository and Codex plugin layout, prefer `../../scripts/generate_image.py --profile count --model gpt-image-2-count`.
- In the source repository and Codex plugin layout, prefer `../../scripts/edit_image.py --profile count --model gpt-image-2-count`.
- Keep the model on `gpt-image-2-count` unless the user explicitly asks for another model.
- Always pass `--output-dir` unless the user explicitly wants files in the current directory.
- Use `--response-path` when the user wants the raw API payload preserved for debugging.
- Use `--mask` when the user wants a localized edit and already has a mask image.
- Read the script JSON output and surface `profile_resolved` plus `api_key_source` when billing-path clarity matters.
- Host-specific release ZIPs rewrite these script paths so each installed bundle stays self-contained.

## Reference

Read `references/api.md` for the count profile environment variable, commands, and request defaults.
