---
name: rootflowai-image
description: Generate or edit images through the RootFlowAI-compatible images API. Use this skill when a user wants Codex to create images with `/v1/images/generations` or transform existing images with `/v1/images/edits`, including setups that use separate API keys for `gpt-image-2` and `gpt-image-2-count`.
---

# RootFlowAI Image

## Overview

Use this skill to generate new images or edit existing images through the RootFlowAI images API.
Prefer the bundled plugin scripts for normal work so auth, request formatting, response parsing, and file saving stay consistent.

## Quick Start

1. Confirm the user has a RootFlowAI API key.
2. Prefer separate profile keys:
   - `ROOTFLOWAI_METERED_API_KEY` for `gpt-image-2`
   - `ROOTFLOWAI_COUNT_API_KEY` for `gpt-image-2-count`
3. Treat the legacy `ROOTFLOWAI_API_KEY` as a backward-compatible alias for the metered profile.
4. Use `generate_image.py` for prompt-to-image work and `edit_image.py` for image-to-image editing.
5. Return the saved file paths to the user.

Example:

```bash
ROOTFLOWAI_METERED_API_KEY=your_metered_key_here \
python3 /absolute/path/to/plugins/rootflowai-image/scripts/generate_image.py \
  --prompt "Three oath brothers doing a short-video livestream" \
  --output-dir /absolute/path/to/output/rootflowai-images
```

```bash
ROOTFLOWAI_COUNT_API_KEY=your_count_key_here \
python3 /absolute/path/to/plugins/rootflowai-image/scripts/generate_image.py \
  --model "gpt-image-2-count" \
  --prompt "Three oath brothers doing a short-video livestream" \
  --output-dir /absolute/path/to/output/rootflowai-images
```

```bash
ROOTFLOWAI_METERED_API_KEY=your_metered_key_here \
python3 /absolute/path/to/plugins/rootflowai-image/scripts/edit_image.py \
  --image /absolute/path/to/portrait.jpg \
  --prompt "Convert this portrait into an American-style professional headshot" \
  --output-dir /absolute/path/to/output/rootflowai-edits
```

## Default Request Settings

Use these defaults unless the user asks for something else:

- generation endpoint: `https://api.rootflowai.com/v1/images/generations`
- edit endpoint: `https://api.rootflowai.com/v1/images/edits`
- metered model: `gpt-image-2`
- count model: `gpt-image-2-count`
- size: `1536x1024`
- quality: `high`
- count: `1`

## Workflow

- Prefer `../../scripts/generate_image.py` for prompt-to-image requests.
- Prefer `../../scripts/edit_image.py` for image editing requests.
- Leave `--profile` as `auto` when the model clearly implies the billing key to use.
- Use `--profile metered` or `--profile count` when the user wants to force a specific billing route regardless of the default model mapping.
- Always pass `--output-dir` unless the user explicitly wants files in the current directory.
- Use `--response-path` when the user wants the raw API payload preserved for debugging.
- Use `--mask` when the user wants a localized inpaint-style edit and already has a mask image.
- If the API returns no usable image data, summarize the response instead of claiming success.
- Only fall back to raw `curl` when debugging request or response mismatches, or when the user explicitly asks for the raw HTTP example.

## Script Behavior

The bundled scripts handle:

- auth from profile-aware env vars or `--api-key`
- automatic profile resolution from model:
  - `gpt-image-2` -> `metered`
  - `gpt-image-2-count` -> `count`
- explicit `--profile auto|metered|count`
- JSON requests for generations
- multipart form-data requests for edits
- response parsing for `b64_json`, `url`, and `image_url`
- downloading remote image URLs when needed
- saving images with inferred file extensions
- optional raw response capture
- JSON output that includes the resolved profile and key source for auditability

## Compatibility Note

The edit flow in this repo is implemented against the OpenAI-compatible `POST /v1/images/edits` contract documented by OpenAI.
In this session, the code was updated to support that contract, but the endpoint was not live-tested against RootFlowAI with a real key and personal image due privacy and credential-handling limits.

## Reference

Read `references/api.md` when you need the exact request body, environment variables, CLI flags, or supported response shapes.
