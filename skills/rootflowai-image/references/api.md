# RootFlowAI Images API Reference

## Endpoint

- default base URL: `https://api.rootflowai.com/v1`
- generation path: `/images/generations`
- full default URL: `https://api.rootflowai.com/v1/images/generations`
- edit path: `/images/edits`
- full edit URL: `https://api.rootflowai.com/v1/images/edits`

## Authentication

The script reads the API key from:

1. `--api-key`
2. `ROOTFLOWAI_API_KEY`

Optional environment variable:

- `ROOTFLOWAI_BASE_URL`

Use `ROOTFLOWAI_BASE_URL` only when the server base URL is different from the production default.

## Default Generation Request Body

```json
{
  "model": "gpt-image-2",
  "prompt": "Three oath brothers doing a short-video livestream",
  "size": "1536x1024",
  "quality": "high",
  "n": 1
}
```

## Default Edit Multipart Fields

- `model=gpt-image-2`
- `prompt=<required prompt>`
- `image=@/absolute/path/to/input.jpg`
- optional `mask=@/absolute/path/to/mask.png`
- optional `size=1536x1024`
- optional `quality=high`
- optional `n=1`

## CLI

```bash
python3 /absolute/path/to/plugins/rootflowai-image/scripts/generate_image.py \
  --prompt "Three oath brothers doing a short-video livestream" \
  --output-dir /absolute/path/to/output
```

```bash
python3 /absolute/path/to/plugins/rootflowai-image/scripts/edit_image.py \
  --image /absolute/path/to/input.jpg \
  --prompt "Convert this portrait into an American-style professional headshot" \
  --output-dir /absolute/path/to/output
```

Useful flags:

- `--image`
- `--mask`
- `--model`
- `--size`
- `--quality`
- `--n`
- `--background`
- `--input-fidelity`
- `--response-path`
- `--prefix`
- `--timeout`

## Supported Response Shapes

The scripts save images from these common fields:

- `data[].b64_json`
- `data[].url`
- `data[].image_url`

If none of those fields are present, the script exits with an error and prints a response summary.

## Raw curl Example: Generations

```bash
curl --location 'https://api.rootflowai.com/v1/images/generations' \
  --header "Authorization: Bearer $ROOTFLOWAI_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-2",
    "prompt": "Three oath brothers doing a short-video livestream",
    "size": "1536x1024",
    "quality": "high",
    "n": 1
  }'
```

## Raw curl Example: Edits

```bash
curl --location 'https://api.rootflowai.com/v1/images/edits' \
  --header "Authorization: Bearer $ROOTFLOWAI_API_KEY" \
  --form 'model=gpt-image-2' \
  --form 'image=@/absolute/path/to/input.jpg' \
  --form 'prompt=Convert this portrait into an American-style professional headshot' \
  --form 'size=1536x1024' \
  --form 'quality=high' \
  --form 'n=1'
```

## Compatibility Note

- The edit implementation in this repository follows OpenAI's documented `POST /v1/images/edits` contract, which supports multipart uploads with `image` and optional `mask`.
- In this session, the edit endpoint was not live-tested against RootFlowAI with a real API key and personal image, so compatibility is implemented but not end-to-end confirmed here.

## Notes

- The script uses Python standard library modules only.
- Remote URL responses are downloaded and saved locally.
- File extensions are inferred from content type, magic bytes, or URL path.
