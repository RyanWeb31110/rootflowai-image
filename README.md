# RootFlowAI Image

`rootflowai-image` is a local Codex plugin that generates and edits images through the RootFlowAI-compatible images API and saves them to disk.

## What It Includes

- `.codex-plugin/plugin.json`: plugin manifest
- `skills/rootflowai-image/`: skill instructions and references
- `scripts/generate_image.py`: CLI for image generation
- `scripts/edit_image.py`: CLI for image editing

## Requirements

- Python 3
- Valid RootFlowAI API key(s)

## Credential Profiles

This repo now supports two billing profiles:

- `metered`: for `gpt-image-2`
- `count`: for `gpt-image-2-count`

Recommended environment variables:

```bash
export ROOTFLOWAI_METERED_API_KEY='your_metered_key'
export ROOTFLOWAI_COUNT_API_KEY='your_count_key'
```

Backward compatibility:

- `ROOTFLOWAI_API_KEY` still works and is treated as the legacy alias for the `metered` profile.

How routing works:

- `--profile auto` is the default
- `gpt-image-2` automatically uses the `metered` profile
- `gpt-image-2-count` automatically uses the `count` profile
- you can override routing explicitly with `--profile metered` or `--profile count`

## Quick Start

Set your API key(s):

```bash
export ROOTFLOWAI_METERED_API_KEY='your_metered_key_here'
export ROOTFLOWAI_COUNT_API_KEY='your_count_key_here'
```

Generate an image with the metered model:

```bash
python3 scripts/generate_image.py \
  --prompt 'Three oath brothers doing a short-video livestream' \
  --output-dir ./out
```

Generate an image with the count-billed model:

```bash
python3 scripts/generate_image.py \
  --model gpt-image-2-count \
  --prompt 'Three oath brothers doing a short-video livestream' \
  --output-dir ./out
```

Edit an existing image:

```bash
python3 scripts/edit_image.py \
  --image /absolute/path/to/portrait.jpg \
  --prompt 'Convert this into an American-style professional corporate headshot' \
  --output-dir ./out
```

## Common Options

```bash
python3 scripts/generate_image.py \
  --prompt 'American-style professional headshot, blue studio background' \
  --size 1536x1024 \
  --quality high \
  --n 2 \
  --output-dir ./out \
  --response-path ./out/response.json
```

```bash
python3 scripts/generate_image.py \
  --profile count \
  --prompt 'Minimal product ad shot on a clean studio set' \
  --output-dir ./out
```

```bash
python3 scripts/edit_image.py \
  --image /absolute/path/to/portrait.jpg \
  --profile count \
  --mask /absolute/path/to/mask.png \
  --prompt 'Replace the background with a blue textured studio backdrop' \
  --size 1536x1024 \
  --quality high \
  --output-dir ./out \
  --response-path ./out/edit-response.json
```

## Files

- Skill entrypoint: `skills/rootflowai-image/SKILL.md`
- API reference: `skills/rootflowai-image/references/api.md`
- Scripts: `scripts/generate_image.py`, `scripts/edit_image.py`

## Notes

- Do not commit API keys into this repository.
- The scripts use Python standard library modules only.
- Both scripts print `profile_resolved` and `api_key_source` in their JSON output so you can see which billing path was actually used.
- The edit flow in this repo is implemented against the OpenAI-compatible `POST /v1/images/edits` contract. It has not been live-tested against RootFlowAI with a real key and image inside this repo automation session.
