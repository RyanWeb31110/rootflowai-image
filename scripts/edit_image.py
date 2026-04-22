#!/usr/bin/env python3
"""Edit existing images through the RootFlowAI-compatible images API."""

from __future__ import annotations

import argparse
import json
import os

from pathlib import Path

from image_api_common import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_QUALITY,
    DEFAULT_SIZE,
    add_profile_arguments,
    get_api_key,
    post_multipart_request,
    resolve_model,
    save_response_images,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Edit images with the RootFlowAI images API and save them to disk."
    )
    parser.add_argument("--prompt", required=True, help="Instruction describing the desired edit.")
    parser.add_argument(
        "--image",
        action="append",
        required=True,
        help="Input image path. Repeat this flag to provide multiple reference images.",
    )
    parser.add_argument(
        "--mask",
        help="Optional mask image path. Transparent areas indicate where edits should be applied.",
    )
    parser.add_argument(
        "--api-key",
        help="Bearer token. Overrides profile-based environment variable resolution.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("ROOTFLOWAI_BASE_URL", DEFAULT_BASE_URL),
        help="API base URL. Defaults to ROOTFLOWAI_BASE_URL or the production URL.",
    )
    parser.add_argument("--model", help=f"Model name. Defaults to {DEFAULT_MODEL}.")
    add_profile_arguments(parser)
    parser.add_argument("--size", default=DEFAULT_SIZE, help="Requested output size.")
    parser.add_argument("--quality", default=DEFAULT_QUALITY, help="Requested output quality.")
    parser.add_argument("--n", type=int, default=1, help="Number of images to request.")
    parser.add_argument(
        "--background",
        help="Optional background mode, if supported by the API.",
    )
    parser.add_argument(
        "--input-fidelity",
        help="Optional input fidelity value, if supported by the API.",
    )
    parser.add_argument(
        "--output-dir",
        default="rootflowai-edits",
        help="Directory where edited images will be saved.",
    )
    parser.add_argument(
        "--prefix",
        default="edit",
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


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    effective_model = resolve_model(args.profile, args.model)

    try:
        api_key, resolved_profile, api_key_source = get_api_key(
            args.api_key,
            profile=args.profile,
            model=effective_model,
        )
    except SystemExit as exc:
        parser.error(str(exc))

    if args.n < 1:
        parser.error("--n must be at least 1.")

    input_paths = [Path(path).expanduser().resolve() for path in args.image]
    for path in input_paths:
        if not path.is_file():
            parser.error(f"Input image not found: {path}")

    mask_path = None
    if args.mask:
        mask_path = Path(args.mask).expanduser().resolve()
        if not mask_path.is_file():
            parser.error(f"Mask image not found: {mask_path}")

    fields = [
        ("model", effective_model),
        ("prompt", args.prompt),
        ("size", args.size),
        ("quality", args.quality),
        ("n", str(args.n)),
    ]
    if args.background:
        fields.append(("background", args.background))
    if args.input_fidelity:
        fields.append(("input_fidelity", args.input_fidelity))

    files = [("image", path) for path in input_paths]
    if mask_path is not None:
        files.append(("mask", mask_path))

    response_payload = post_multipart_request(
        endpoint="/images/edits",
        api_key=api_key,
        base_url=args.base_url,
        fields=fields,
        files=files,
        timeout=args.timeout,
        error_label="Image edit request failed.",
    )

    saved_paths, skipped_items, raw_response_path = save_response_images(
        response_payload=response_payload,
        output_dir=args.output_dir,
        prefix=args.prefix,
        timeout=args.timeout,
        response_path=args.response_path,
    )

    print(
        json.dumps(
            {
                "saved": saved_paths,
                "skipped_items": skipped_items,
                "response_path": raw_response_path,
                "model": effective_model,
                "profile_requested": args.profile,
                "profile_resolved": resolved_profile,
                "api_key_source": api_key_source,
                "size": args.size,
                "quality": args.quality,
                "n_requested": args.n,
                "n_saved": len(saved_paths),
                "input_images": [str(path) for path in input_paths],
                "mask": str(mask_path) if mask_path else None,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
