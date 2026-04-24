---
name: rootflowai-image-count
description: Generate or edit images through the RootFlowAI-compatible images API using the count-billed lane. Supports 1K/2K/4K resolution tiers and image-to-image. Use this skill when the user wants the `gpt-image-2-count` model, the count API key, or a separate per-request billing workflow.
---

# RootFlowAI Image Count

## Overview

Use this skill for the count-billed RootFlowAI image workflow.
It should prefer the `gpt-image-2-count` model and the count credential profile unless the user explicitly asks for something else.

## Models

| Model | Resolution | Notes |
|-------|-----------|-------|
| `gpt-image-2-count` | 1K (default) | All 13 size ratios |
| `gpt-image-2-hd-count` | 2K | All 13 size ratios |
| `gpt-image-2-4k-count` | 4K | Only `16:9`/`9:16`/`2:1`/`1:2`/`21:9`/`9:21` |

## Quick Start

1. Use `ROOTFLOWAI_COUNT_API_KEY` for authentication.
2. Use `generate_image.py` for text-to-image and image-to-image work.
3. Use `edit_image.py` for image editing work (multipart upload).
4. Pass `--profile count` so the billing route stays explicit.
5. Prefer `gpt-image-2-count` as the default model; use `gpt-image-2-hd-count` for 2K or `gpt-image-2-4k-count` for 4K.

Text-to-image:

```bash
ROOTFLOWAI_COUNT_API_KEY=your_count_key_here \
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-count \
  --prompt "Three oath brothers doing a short-video livestream" \
  --size "16:9" \
  --output-dir ./out
```

Text-to-image (2K):

```bash
ROOTFLOWAI_COUNT_API_KEY=your_count_key_here \
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-hd-count \
  --prompt "A cinematic sunset over the ocean" \
  --size "16:9" \
  --output-dir ./out
```

Image-to-image:

```bash
ROOTFLOWAI_COUNT_API_KEY=your_count_key_here \
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-count \
  --prompt "Convert this into oil painting style" \
  --image https://example.com/photo.png \
  --size "1:1" \
  --output-dir ./out
```

Image edit (multipart):

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

## Size

Use ratio format: `1:1`, `3:2`, `2:3`, `4:3`, `3:4`, `5:4`, `4:5`, `16:9`, `9:16`, `2:1`, `1:2`, `21:9`, `9:21`.

Pixel formats (e.g. `1024x1024`) are also accepted and auto-converted to the nearest ratio.

## Workflow

- In the source repository and Codex plugin layout, prefer `../../scripts/generate_image.py --profile count --model gpt-image-2-count`.
- In the source repository and Codex plugin layout, prefer `../../scripts/edit_image.py --profile count --model gpt-image-2-count`.
- For image-to-image, use `generate_image.py` with `--image` (URL or local path). Repeat `--image` for multiple reference images (up to 16).
- Keep the model on `gpt-image-2-count` unless the user explicitly asks for HD or 4K.
- Always pass `--output-dir` unless the user explicitly wants files in the current directory.
- Use `--response-path` when the user wants the raw API payload preserved for debugging.
- Use `--mask` with `edit_image.py` when the user wants a localized edit and already has a mask image.
- Read the script JSON output and surface `profile_resolved` plus `api_key_source` when billing-path clarity matters.
- Host-specific release ZIPs rewrite these script paths so each installed bundle stays self-contained.

## Reference

Read `references/api.md` for the count profile environment variable, commands, and request defaults.
