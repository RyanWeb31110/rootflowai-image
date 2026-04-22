# RootFlowAI Count API Reference

## Use Case

Use this skill when you want the count-billed workflow.

- profile: `count`
- preferred model: `gpt-image-2-count`
- preferred env var: `ROOTFLOWAI_COUNT_API_KEY`

## Environment

```bash
export ROOTFLOWAI_COUNT_API_KEY='your_count_key_here'
```

## Generate

```bash
python3 /absolute/path/to/rootflowai-image/scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-count \
  --prompt "Three oath brothers doing a short-video livestream" \
  --output-dir /absolute/path/to/output
```

## Edit

```bash
python3 /absolute/path/to/rootflowai-image/scripts/edit_image.py \
  --profile count \
  --model gpt-image-2-count \
  --image /absolute/path/to/portrait.jpg \
  --prompt "Convert this portrait into an American-style professional headshot" \
  --output-dir /absolute/path/to/output
```

## Defaults

- generation path: `/images/generations`
- edit path: `/images/edits`
- model: `gpt-image-2-count`
- size: `1536x1024`
- quality: `high`

## Notes

- `--api-key` overrides env-based profile resolution.
- Script output includes `profile_requested`, `profile_resolved`, and `api_key_source`.
