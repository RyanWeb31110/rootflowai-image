#!/usr/bin/env python3
"""Generate images through the RootFlowAI-compatible images API."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib import error, parse, request

DEFAULT_BASE_URL = "https://api.rootflowai.com/v1"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1536x1024"
DEFAULT_QUALITY = "high"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate images with the RootFlowAI images API and save them to disk."
    )
    parser.add_argument("--prompt", required=True, help="Text prompt for image generation.")
    parser.add_argument(
        "--api-key",
        help="Bearer token. Defaults to the ROOTFLOWAI_API_KEY environment variable.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("ROOTFLOWAI_BASE_URL", DEFAULT_BASE_URL),
        help="API base URL. Defaults to ROOTFLOWAI_BASE_URL or the production URL.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name.")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="Requested image size.")
    parser.add_argument("--quality", default=DEFAULT_QUALITY, help="Requested image quality.")
    parser.add_argument("--n", type=int, default=1, help="Number of images to request.")
    parser.add_argument(
        "--output-dir",
        default="rootflowai-images",
        help="Directory where generated images will be saved.",
    )
    parser.add_argument(
        "--prefix",
        default="image",
        help="Filename prefix used for saved images.",
    )
    parser.add_argument(
        "--response-path",
        help="Optional path where the raw JSON response will be saved.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=180.0,
        help="HTTP timeout in seconds.",
    )
    return parser


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def infer_extension(data: bytes, content_type: str | None = None, source_url: str | None = None) -> str:
    if content_type:
        content_type = content_type.lower()
        if "png" in content_type:
            return ".png"
        if "jpeg" in content_type or "jpg" in content_type:
            return ".jpg"
        if "webp" in content_type:
            return ".webp"
        if "gif" in content_type:
            return ".gif"
        if "bmp" in content_type:
            return ".bmp"

    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return ".gif"
    if data.startswith(b"BM"):
        return ".bmp"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ".webp"

    if source_url:
        suffix = Path(parse.urlparse(source_url).path).suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}:
            return ".jpg" if suffix == ".jpeg" else suffix

    return ".bin"


def fetch_url(url: str, timeout: float) -> tuple[bytes, str | None]:
    req = request.Request(url, method="GET")
    with request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        return data, resp.headers.get_content_type()


def load_image_bytes(item: dict[str, Any], timeout: float) -> tuple[bytes, str | None, str | None]:
    for key in ("b64_json", "image_base64", "base64", "b64"):
        value = item.get(key)
        if isinstance(value, str) and value:
            return base64.b64decode(value), None, None

    for key in ("url", "image_url"):
        value = item.get(key)
        if isinstance(value, str) and value:
            data, content_type = fetch_url(value, timeout)
            return data, content_type, value

    raise ValueError("Response item does not contain a supported image field.")


def save_raw_response(response_path: str, payload: dict[str, Any]) -> str:
    path = Path(response_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return str(path)


def post_generation_request(
    api_key: str,
    base_url: str,
    payload: dict[str, Any],
    timeout: float,
) -> dict[str, Any]:
    url = f"{normalize_base_url(base_url)}/images/generations"
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = request.Request(url, data=body, headers=headers, method="POST")

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        print(
            json.dumps(
                {
                    "error": "Image generation request failed.",
                    "status": exc.code,
                    "response": error_body,
                },
                ensure_ascii=True,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    except error.URLError as exc:
        print(
            json.dumps(
                {
                    "error": "Could not reach the RootFlowAI API.",
                    "reason": str(exc.reason),
                },
                ensure_ascii=True,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    try:
        payload_data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(
            json.dumps(
                {
                    "error": "API returned a non-JSON response.",
                    "response": raw,
                },
                ensure_ascii=True,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    if not isinstance(payload_data, dict):
        print(
            json.dumps(
                {
                    "error": "API returned an unexpected JSON shape.",
                    "response": payload_data,
                },
                ensure_ascii=True,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)

    return payload_data


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ROOTFLOWAI_API_KEY")
    if not api_key:
        parser.error("Missing API key. Use --api-key or set ROOTFLOWAI_API_KEY.")

    if args.n < 1:
        parser.error("--n must be at least 1.")

    request_payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "quality": args.quality,
        "n": args.n,
    }
    response_payload = post_generation_request(
        api_key=api_key,
        base_url=args.base_url,
        payload=request_payload,
        timeout=args.timeout,
    )

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_response_path = None
    if args.response_path:
        raw_response_path = save_raw_response(args.response_path, response_payload)

    items = response_payload.get("data")
    if not isinstance(items, list) or not items:
        print(
            json.dumps(
                {
                    "error": "API response does not contain a non-empty data array.",
                    "response_path": raw_response_path,
                    "response": response_payload,
                },
                ensure_ascii=True,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1

    saved_paths: list[str] = []
    skipped_items: list[int] = []

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            skipped_items.append(index)
            continue

        try:
            image_bytes, content_type, source_url = load_image_bytes(item, args.timeout)
        except Exception:
            skipped_items.append(index)
            continue

        extension = infer_extension(image_bytes, content_type=content_type, source_url=source_url)
        output_path = output_dir / f"{args.prefix}-{index:02d}{extension}"
        output_path.write_bytes(image_bytes)
        saved_paths.append(str(output_path))

    if not saved_paths:
        print(
            json.dumps(
                {
                    "error": "API responded, but no image files could be extracted.",
                    "response_path": raw_response_path,
                    "response": response_payload,
                },
                ensure_ascii=True,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1

    print(
        json.dumps(
            {
                "saved": saved_paths,
                "skipped_items": skipped_items,
                "response_path": raw_response_path,
                "model": args.model,
                "size": args.size,
                "quality": args.quality,
                "n_requested": args.n,
                "n_saved": len(saved_paths),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
