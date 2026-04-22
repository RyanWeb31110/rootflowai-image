from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "build_release_packages.py"

SPEC = importlib.util.spec_from_file_location("build_release_packages", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
build_release_packages = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_release_packages
SPEC.loader.exec_module(build_release_packages)


class BuildReleasePackagesTests(unittest.TestCase):
    def test_rewrite_script_paths_rewrites_repo_paths(self) -> None:
        source = (
            "Use `../../scripts/generate_image.py`.\n"
            "python3 ../../scripts/edit_image.py\n"
        )
        rewritten = build_release_packages.rewrite_script_paths(source, "scripts/")
        self.assertIn("`scripts/generate_image.py`", rewritten)
        self.assertIn("python3 scripts/edit_image.py", rewritten)
        self.assertNotIn("../../scripts/", rewritten)

    def test_openclaw_frontmatter_includes_primary_env_metadata(self) -> None:
        source = (
            "---\n"
            "name: rootflowai-image-metered\n"
            "description: demo\n"
            "---\n"
            "\n"
            "Body\n"
        )
        rewritten = build_release_packages.inject_openclaw_frontmatter(
            source,
            "ROOTFLOWAI_METERED_API_KEY",
        )
        self.assertIn("homepage: https://github.com/RyanWeb31110/rootflowai-image", rewritten)
        self.assertIn('"primaryEnv":"ROOTFLOWAI_METERED_API_KEY"', rewritten)

    def test_cherry_studio_bundle_is_self_contained_without_agents(self) -> None:
        target = next(spec for spec in build_release_packages.TARGET_SPECS if spec.name == "cherry-studio")
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            artifacts = build_release_packages.build_skill_target(output_dir, target)
            self.assertEqual(len(artifacts), 2)

            bundle_dir = output_dir / "cherry-studio" / "rootflowai-image-metered"
            self.assertTrue((bundle_dir / "SKILL.md").is_file())
            self.assertTrue((bundle_dir / "scripts" / "generate_image.py").is_file())
            self.assertTrue((bundle_dir / "references" / "api.md").is_file())
            self.assertFalse((bundle_dir / "agents").exists())
            self.assertFalse((bundle_dir / "scripts" / "build_release_packages.py").exists())
            self.assertTrue((output_dir / artifacts[0]["zip"]).is_file())

    def test_codex_skill_bundle_keeps_agents_metadata(self) -> None:
        target = next(spec for spec in build_release_packages.TARGET_SPECS if spec.name == "codex-skill")
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            build_release_packages.build_skill_target(output_dir, target)

            bundle_dir = output_dir / "codex-skill" / "rootflowai-image-count"
            self.assertTrue((bundle_dir / "agents" / "openai.yaml").is_file())
            self.assertTrue((bundle_dir / "scripts" / "edit_image.py").is_file())

    def test_openclaw_bundle_uses_base_dir_and_no_agents(self) -> None:
        target = next(spec for spec in build_release_packages.TARGET_SPECS if spec.name == "openclaw")
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            build_release_packages.build_skill_target(output_dir, target)

            bundle_dir = output_dir / "openclaw" / "rootflowai-image-metered"
            content = (bundle_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("{baseDir}/scripts/generate_image.py", content)
            self.assertIn('"primaryEnv":"ROOTFLOWAI_METERED_API_KEY"', content)
            self.assertFalse((bundle_dir / "agents").exists())


if __name__ == "__main__":
    unittest.main()
