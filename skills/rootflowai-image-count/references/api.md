# RootFlowAI Count API Reference

## Use Case

Use this skill when you want the count-billed workflow.

- profile: `count`
- preferred model: `gpt-image-2-count`
- HD model: `gpt-image-2-hd-count` (2K)
- 4K model: `gpt-image-2-4k-count` (4K, limited size ratios)
- Gemini models:
  - `gemini-2.5-flash-image-count` (1K)
  - `gemini-3.1-flash-image-count` / `gemini-3.1-flash-image-hd-count` / `gemini-3.1-flash-image-4k-count`
  - `gemini-3-pro-image-count` / `gemini-3-pro-image-hd-count` / `gemini-3-pro-image-4k-count`
- preferred env var: `ROOTFLOWAI_COUNT_API_KEY`

## Environment

```bash
export ROOTFLOWAI_COUNT_API_KEY='your_count_key_here'
```

## Generate (text-to-image)

```bash
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-count \
  --prompt "Three oath brothers doing a short-video livestream" \
  --size "16:9" \
  --output-dir ./out
```

## Generate (2K)

```bash
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-hd-count \
  --prompt "A cinematic sunset over the ocean" \
  --size "16:9" \
  --output-dir ./out
```

## Generate (image-to-image)

```bash
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-count \
  --prompt "Convert this into watercolor style" \
  --image https://example.com/photo.png \
  --size "1:1" \
  --output-dir ./out
```

## Generate (Gemini)

Use Gemini when the user asks for Gemini/Nano Banana, character consistency, style consistency, or an explicit Gemini model.
Still use the count profile and `ROOTFLOWAI_COUNT_API_KEY`.

```bash
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gemini-3.1-flash-image-count \
  --prompt "A clean product hero image for a black ceramic coffee cup" \
  --size "1:1" \
  --output-dir ./out
```

Gemini 4K:

```bash
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gemini-3-pro-image-4k-count \
  --prompt "A premium watch campaign poster, studio lighting, crisp detail" \
  --size "1:1" \
  --output-dir ./out
```

Multiple reference images (up to 16):

```bash
python3 ../../scripts/generate_image.py \
  --profile count \
  --model gpt-image-2-count \
  --prompt "Merge these two photos into a poster" \
  --image https://example.com/photo-a.png \
  --image /local/path/to/photo-b.png \
  --size "4:3" \
  --output-dir ./out
```

## Edit (multipart upload)

```bash
python3 ../../scripts/edit_image.py \
  --profile count \
  --model gpt-image-2-count \
  --image /absolute/path/to/portrait.jpg \
  --prompt "Convert this portrait into an American-style professional headshot" \
  --output-dir ./out
```

## Defaults

- generation path: `/images/generations`
- edit path: `/images/edits`
- model: `gpt-image-2-count`
- size: `1536x1024`

## Size

Ratio format: `1:1`, `3:2`, `2:3`, `4:3`, `3:4`, `5:4`, `4:5`, `16:9`, `9:16`, `2:1`, `1:2`, `21:9`, `9:21`.

4K only supports: `16:9`, `9:16`, `2:1`, `1:2`, `21:9`, `9:21`.

Pixel formats (e.g. `1024x1024`) are also accepted and auto-converted.

## Notes

- `--api-key` overrides env-based profile resolution.
- `--image` in `generate_image.py` accepts URLs (https) or local file paths. Local files are sent as base64 data URIs.
- Gemini count models automatically use the count profile in `--profile auto`.
- Gemini models do not use `quality`; the scripts omit that parameter for Gemini requests.
- `gemini-2.5-flash-image-count` is 1K only. Use Gemini 3.1 Flash or Gemini 3 Pro for 2K/4K.
- Script output includes `profile_requested`, `profile_resolved`, and `api_key_source`.
- Installed skill ZIPs bundle the runtime scripts inside the skill; the source repository and plugin layout keep the canonical runtime files in the top-level `scripts/` directory.
