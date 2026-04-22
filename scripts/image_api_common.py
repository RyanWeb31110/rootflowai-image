"""Shared helpers for the RootFlowAI image API scripts."""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from typing import Any
from urllib import error, parse, request

DEFAULT_BASE_URL = "https://api.rootflowai.com/v1"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1536x1024"
DEFAULT_QUALITY = "high"


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def infer_extension(
    data: bytes,
    content_type: str | None = None,
    source_url: str | None = None,
) -> str:
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


def parse_json_response(raw: str) -> dict[str, Any]:
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


def perform_request(
    req: request.Request,
    timeout: float,
    error_label: str,
) -> dict[str, Any]:
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        print(
            json.dumps(
                {
                    "error": error_label,
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

    return parse_json_response(raw)


def post_json_request(
    endpoint: str,
    api_key: str,
    base_url: str,
    payload: dict[str, Any],
    timeout: float,
    error_label: str,
) -> dict[str, Any]:
    url = f"{normalize_base_url(base_url)}{endpoint}"
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = request.Request(url, data=body, headers=headers, method="POST")
    return perform_request(req, timeout, error_label)


def encode_multipart_form_data(
    fields: list[tuple[str, str]],
    files: list[tuple[str, Path]],
) -> tuple[bytes, str]:
    boundary = f"----rootflowaiimage{uuid.uuid4().hex}"
    body = bytearray()

    for name, value in fields:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")

    for field_name, file_path in files:
        file_bytes = file_path.read_bytes()
        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            (
                f'Content-Disposition: form-data; name="{field_name}"; '
                f'filename="{file_path.name}"\r\n'
            ).encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(file_bytes)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return bytes(body), f"multipart/form-data; boundary={boundary}"


def post_multipart_request(
    endpoint: str,
    api_key: str,
    base_url: str,
    fields: list[tuple[str, str]],
    files: list[tuple[str, Path]],
    timeout: float,
    error_label: str,
) -> dict[str, Any]:
    url = f"{normalize_base_url(base_url)}{endpoint}"
    body, content_type = encode_multipart_form_data(fields, files)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": content_type,
        "Content-Length": str(len(body)),
    }
    req = request.Request(url, data=body, headers=headers, method="POST")
    return perform_request(req, timeout, error_label)


def save_response_images(
    response_payload: dict[str, Any],
    output_dir: str,
    prefix: str,
    timeout: float,
    response_path: str | None = None,
) -> tuple[list[str], list[int], str | None]:
    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    raw_response_path = None
    if response_path:
        raw_response_path = save_raw_response(response_path, response_payload)

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
        raise SystemExit(1)

    saved_paths: list[str] = []
    skipped_items: list[int] = []

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            skipped_items.append(index)
            continue

        try:
            image_bytes, content_type, source_url = load_image_bytes(item, timeout)
        except Exception:
            skipped_items.append(index)
            continue

        extension = infer_extension(image_bytes, content_type=content_type, source_url=source_url)
        file_path = output_path / f"{prefix}-{index:02d}{extension}"
        file_path.write_bytes(image_bytes)
        saved_paths.append(str(file_path))

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
        raise SystemExit(1)

    return saved_paths, skipped_items, raw_response_path


def get_api_key(explicit_api_key: str | None) -> str:
    api_key = explicit_api_key or os.environ.get("ROOTFLOWAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing API key. Use --api-key or set ROOTFLOWAI_API_KEY.")
    return api_key
