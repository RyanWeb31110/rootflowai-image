---
name: rootflowai-image
description: Generate images through the RootFlowAI-compatible images API. Use this skill when a user wants Codex to create or iterate images with `https://api.rootflowai.com/v1/images/generations`, especially when they already have a Bearer token and want a repeatable local workflow that saves files to disk.
---

# RootFlowAI Image

## Overview

Use this skill to generate one or more images from a text prompt through the RootFlowAI images API.
Prefer the bundled plugin script for normal work so auth, request formatting, response parsing, and file saving stay consistent.

## Quick Start

1. Confirm the user has a RootFlowAI API key.
2. Use `ROOTFLOWAI_API_KEY` for auth unless the user explicitly wants to pass the key as a CLI flag.
3. Run the bundled script with an explicit prompt and output directory.
4. Return the saved file paths to the user.

Example:

```bash
ROOTFLOWAI_API_KEY=your_token_here \
python3 /absolute/path/to/plugins/rootflowai-image/scripts/generate_image.py \
  --prompt "Three oath brothers doing a short-video livestream" \
  --output-dir /absolute/path/to/output/rootflowai-images
```

## Default Request Settings

Use these defaults unless the user asks for something else:

- endpoint: `https://api.rootflowai.com/v1/images/generations`
- model: `gpt-image-2`
- size: `1536x1024`
- quality: `high`
- count: `1`

## Workflow

- Prefer `../../scripts/generate_image.py` relative to this skill folder for standard image generation requests.
- Always pass `--output-dir` unless the user explicitly wants files in the current directory.
- Use `--response-path` when the user wants the raw API payload preserved for debugging.
- If the API returns no usable image data, summarize the response instead of claiming success.
- Only fall back to raw `curl` when debugging request or response mismatches, or when the user explicitly asks for the raw HTTP example.

## Script Behavior

The bundled script handles:

- auth from `ROOTFLOWAI_API_KEY` or `--api-key`
- JSON request assembly
- response parsing for `b64_json`, `url`, and `image_url`
- downloading remote image URLs when needed
- saving images with inferred file extensions
- optional raw response capture

## Reference

Read `references/api.md` when you need the exact request body, environment variables, CLI flags, or supported response shapes.
