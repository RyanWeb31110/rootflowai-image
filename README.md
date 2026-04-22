# RootFlowAI Image

`rootflowai-image` is a local Codex plugin that generates images through the RootFlowAI-compatible images API and saves them to disk.

## What It Includes

- `.codex-plugin/plugin.json`: plugin manifest
- `skills/rootflowai-image/`: skill instructions and references
- `scripts/generate_image.py`: CLI for image generation

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

## Files

- Skill entrypoint: `skills/rootflowai-image/SKILL.md`
- API reference: `skills/rootflowai-image/references/api.md`
- Script: `scripts/generate_image.py`

## Notes

- Do not commit API keys into this repository.
- The script uses Python standard library modules only.
