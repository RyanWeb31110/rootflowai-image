from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import image_api_common


def public_resolver(_hostname, _port, type=None):  # noqa: A002
    return [
        (None, None, None, None, ("93.184.216.34", 443)),
    ]


def private_resolver(_hostname, _port, type=None):  # noqa: A002
    return [
        (None, None, None, None, ("127.0.0.1", 443)),
    ]


class ValidateRemoteImageUrlTests(unittest.TestCase):
    def test_allows_https_public_address(self) -> None:
        image_api_common.validate_remote_image_url(
            "https://example.com/image.png",
            resolver=public_resolver,
        )

    def test_rejects_non_https(self) -> None:
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            image_api_common.validate_remote_image_url(
                "http://example.com/image.png",
                resolver=public_resolver,
            )

    def test_rejects_localhost(self) -> None:
        with self.assertRaisesRegex(ValueError, "Localhost"):
            image_api_common.validate_remote_image_url(
                "https://localhost/image.png",
                resolver=public_resolver,
            )

    def test_rejects_private_address_resolution(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-public"):
            image_api_common.validate_remote_image_url(
                "https://example.com/image.png",
                resolver=private_resolver,
            )


class ProfileRoutingTests(unittest.TestCase):
    def test_auto_profile_uses_metered_model_by_default(self) -> None:
        self.assertEqual(
            image_api_common.resolve_model(image_api_common.PROFILE_AUTO, None),
            image_api_common.DEFAULT_MODEL,
        )
        self.assertEqual(
            image_api_common.resolve_profile(image_api_common.PROFILE_AUTO, image_api_common.DEFAULT_MODEL),
            image_api_common.PROFILE_METERED,
        )

    def test_count_profile_defaults_to_count_model(self) -> None:
        self.assertEqual(
            image_api_common.resolve_model(image_api_common.PROFILE_COUNT, None),
            image_api_common.COUNT_MODEL,
        )

    def test_get_api_key_uses_profile_specific_env_var(self) -> None:
        with mock.patch.dict(os.environ, {"ROOTFLOWAI_COUNT_API_KEY": "count-demo"}, clear=True):
            key, profile, source = image_api_common.get_api_key(
                None,
                profile=image_api_common.PROFILE_COUNT,
                model=image_api_common.COUNT_MODEL,
            )
        self.assertEqual(key, "count-demo")
        self.assertEqual(profile, image_api_common.PROFILE_COUNT)
        self.assertEqual(source, "ROOTFLOWAI_COUNT_API_KEY")

    def test_metered_profile_falls_back_to_legacy_env_var(self) -> None:
        env = {"ROOTFLOWAI_API_KEY": "legacy-metered-demo"}
        with mock.patch.dict(os.environ, env, clear=True):
            key, profile, source = image_api_common.get_api_key(
                None,
                profile=image_api_common.PROFILE_METERED,
                model=image_api_common.DEFAULT_MODEL,
            )
        self.assertEqual(key, "legacy-metered-demo")
        self.assertEqual(profile, image_api_common.PROFILE_METERED)
        self.assertEqual(source, "ROOTFLOWAI_API_KEY")
