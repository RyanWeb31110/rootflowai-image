---
name: rootflowai-image-metered
description: Generate or edit images through the RootFlowAI-compatible images API using the metered billing lane. Supports image-to-image. Use this skill when the user wants the standard `gpt-image-2` model, the metered API key, or the default non-count workflow.
---

# RootFlowAI Image Metered

## Overview

Use this skill for the standard metered RootFlowAI image workflow.
It should prefer the `gpt-image-2` model and the metered credential profile unless the user explicitly asks for something else.

## Quick Start

1. Prefer `ROOTFLOWAI_METERED_API_KEY` for authentication.
2. Accept the legacy `ROOTFLOWAI_API_KEY` as a backward-compatible alias for this same metered lane.
3. Use `generate_image.py` for text-to-image and image-to-image work.
4. Use `edit_image.py` for image editing work (multipart upload).
5. Pass `--profile metered` so the billing route stays explicit.

Text-to-image:

```bash
ROOTFLOWAI_METERED_API_KEY=your_metered_key_here \
python3 ../../scripts/generate_image.py \
  --profile metered \
  --prompt "Three oath brothers doing a short-video livestream" \
  --size "16:9" \
  --output-dir ./out
```

Image-to-image:

```bash
ROOTFLOWAI_METERED_API_KEY=your_metered_key_here \
python3 ../../scripts/generate_image.py \
  --profile metered \
  --prompt "Convert this into oil painting style" \
  --image https://example.com/photo.png \
  --size "1:1" \
  --output-dir ./out
```

Image edit (multipart):

```bash
ROOTFLOWAI_METERED_API_KEY=your_metered_key_here \
python3 ../../scripts/edit_image.py \
  --profile metered \
  --image /absolute/path/to/portrait.jpg \
  --prompt "Convert this portrait into an American-style professional headshot" \
  --output-dir ./out
```

## Defaults

- generation endpoint: `https://api.rootflowai.com/v1/images/generations`
- edit endpoint: `https://api.rootflowai.com/v1/images/edits`
- profile: `metered`
- model: `gpt-image-2`
- size: `1536x1024`

## Size

Use ratio format: `1:1`, `3:2`, `2:3`, `4:3`, `3:4`, `5:4`, `4:5`, `16:9`, `9:16`, `2:1`, `1:2`, `21:9`, `9:21`.

Pixel formats (e.g. `1024x1024`) are also accepted and auto-converted to the nearest ratio.

## Workflow

- In the source repository and Codex plugin layout, prefer `../../scripts/generate_image.py --profile metered`.
- In the source repository and Codex plugin layout, prefer `../../scripts/edit_image.py --profile metered`.
- For image-to-image, use `generate_image.py` with `--image` (URL or local path). Repeat `--image` for multiple reference images (up to 16).
- Keep the model on `gpt-image-2` unless the user explicitly requests another model.
- Always pass `--output-dir` unless the user explicitly wants files in the current directory.
- Use `--response-path` when the user wants the raw API payload preserved for debugging.
- Use `--mask` with `edit_image.py` when the user wants a localized edit and already has a mask image.
- Read the script JSON output and surface `profile_resolved` plus `api_key_source` when billing-path clarity matters.
- Host-specific release ZIPs rewrite these script paths so each installed bundle stays self-contained.

## Reference

Read `references/api.md` for the metered environment variables, commands, and request defaults.
