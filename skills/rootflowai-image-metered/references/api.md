# RootFlowAI Metered API Reference

## Use Case

Use this skill when you want the standard metered workflow.

- profile: `metered`
- preferred model: `gpt-image-2`
- preferred env var: `ROOTFLOWAI_METERED_API_KEY`
- legacy alias: `ROOTFLOWAI_API_KEY`

## Environment

```bash
export ROOTFLOWAI_METERED_API_KEY='your_metered_key_here'
```

## Generate

```bash
python3 ../../scripts/generate_image.py \
  --profile metered \
  --prompt "Three oath brothers doing a short-video livestream" \
  --output-dir ./out
```

## Edit

```bash
python3 ../../scripts/edit_image.py \
  --profile metered \
  --image /absolute/path/to/portrait.jpg \
  --prompt "Convert this portrait into an American-style professional headshot" \
  --output-dir ./out
```

## Defaults

- generation path: `/images/generations`
- edit path: `/images/edits`
- model: `gpt-image-2`
- size: `1536x1024`
- quality: `high`

## Notes

- `--api-key` overrides env-based profile resolution.
- Script output includes `profile_requested`, `profile_resolved`, and `api_key_source`.
- Installed skill ZIPs bundle the runtime scripts inside the skill; the source repository and plugin layout keep the canonical runtime files in the top-level `scripts/` directory.
