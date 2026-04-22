# RootFlowAI Images API Reference

## Endpoint

- default base URL: `https://api.rootflowai.com/v1`
- generation path: `/images/generations`
- full default URL: `https://api.rootflowai.com/v1/images/generations`

## Authentication

The script reads the API key from:

1. `--api-key`
2. `ROOTFLOWAI_API_KEY`

Optional environment variable:

- `ROOTFLOWAI_BASE_URL`

Use `ROOTFLOWAI_BASE_URL` only when the server base URL is different from the production default.

## Default Request Body

```json
{
  "model": "gpt-image-2",
  "prompt": "Three oath brothers doing a short-video livestream",
  "size": "1536x1024",
  "quality": "high",
  "n": 1
}
```

## CLI

```bash
python3 /absolute/path/to/plugins/rootflowai-image/scripts/generate_image.py \
  --prompt "Three oath brothers doing a short-video livestream" \
  --output-dir /absolute/path/to/output
```

Useful flags:

- `--model`
- `--size`
- `--quality`
- `--n`
- `--response-path`
- `--prefix`
- `--timeout`

## Supported Response Shapes

The script saves images from these common fields:

- `data[].b64_json`
- `data[].url`
- `data[].image_url`

If none of those fields are present, the script exits with an error and prints a response summary.

## Raw curl Example

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

## Notes

- The script uses Python standard library modules only.
- Remote URL responses are downloaded and saved locally.
- File extensions are inferred from content type, magic bytes, or URL path.
