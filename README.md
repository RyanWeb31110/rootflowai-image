# RootFlowAI Image

`rootflowai-image` is a local Codex plugin that generates and edits images through the RootFlowAI-compatible images API and saves them to disk.

## What It Includes

- `.codex-plugin/plugin.json`: plugin manifest
- `skills/rootflowai-image/`: skill instructions and references
- `scripts/generate_image.py`: CLI for image generation
- `scripts/edit_image.py`: CLI for image editing

## Requirements

- Python 3
- A valid RootFlowAI API key

## Quick Start

Set your API key:

```bash
export ROOTFLOWAI_API_KEY='your_api_key_here'
```

Generate an image:

```bash
python3 scripts/generate_image.py \
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
python3 scripts/edit_image.py \
  --image /absolute/path/to/portrait.jpg \
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
- The edit flow in this repo is implemented against the OpenAI-compatible `POST /v1/images/edits` contract. It has not been live-tested against RootFlowAI with a real key and image inside this repo automation session.
