#!/usr/bin/env python3
"""Build self-contained release packages for Codex, Cherry Studio, and Claude-compatible hosts."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
PLUGIN_ROOT = REPO_ROOT / ".codex-plugin"
COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
RUNTIME_SCRIPT_NAMES = (
    "image_api_common.py",
    "generate_image.py",
    "edit_image.py",
)


@dataclass(frozen=True)
class SkillSpec:
    name: str
    source_dir: Path


@dataclass(frozen=True)
class TargetSpec:
    name: str
    include_agents: bool
    package_kind: str


SKILL_SPECS = (
    SkillSpec("rootflowai-image-metered", SKILLS_ROOT / "rootflowai-image-metered"),
    SkillSpec("rootflowai-image-count", SKILLS_ROOT / "rootflowai-image-count"),
)

TARGET_SPECS = (
    TargetSpec("codex-skill", include_agents=True, package_kind="skill"),
    TargetSpec("cherry-studio", include_agents=False, package_kind="skill"),
    TargetSpec("claude-compatible", include_agents=False, package_kind="skill"),
    TargetSpec("codex-plugin", include_agents=True, package_kind="plugin"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Directory where expanded folders and ZIP files will be written.",
    )
    return parser.parse_args()


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def rewrite_for_standalone_bundle(text: str) -> str:
    replacements = {
        "python3 /absolute/path/to/rootflowai-image/scripts/": "python3 scripts/",
        "`../../scripts/": "`scripts/",
        " `../../scripts/": " `scripts/",
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text


def copy_runtime_scripts(destination_dir: Path) -> None:
    destination_dir.mkdir(parents=True, exist_ok=True)
    for script_name in RUNTIME_SCRIPT_NAMES:
        copy_file(SCRIPTS_ROOT / script_name, destination_dir / script_name)


def copy_skill_bundle(target_dir: Path, skill: SkillSpec, include_agents: bool) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    copy_file(skill.source_dir / "SKILL.md", target_dir / "SKILL.md")
    copy_file(skill.source_dir / "references" / "api.md", target_dir / "references" / "api.md")

    if include_agents and (skill.source_dir / "agents").is_dir():
        shutil.copytree(skill.source_dir / "agents", target_dir / "agents", dirs_exist_ok=True, ignore=COPY_IGNORE)

    copy_runtime_scripts(target_dir / "scripts")

    skill_md = rewrite_for_standalone_bundle((target_dir / "SKILL.md").read_text(encoding="utf-8"))
    (target_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    api_md = rewrite_for_standalone_bundle((target_dir / "references" / "api.md").read_text(encoding="utf-8"))
    (target_dir / "references" / "api.md").write_text(api_md, encoding="utf-8")


def build_skill_target(output_dir: Path, target: TargetSpec) -> list[dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    target_root = output_dir / target.name
    target_root.mkdir(parents=True, exist_ok=True)

    for skill in SKILL_SPECS:
        expanded_dir = target_root / skill.name
        if expanded_dir.exists():
            shutil.rmtree(expanded_dir)
        copy_skill_bundle(expanded_dir, skill, include_agents=target.include_agents)

        zip_base = target_root / f"{skill.name}-{target.name}"
        archive_path = shutil.make_archive(str(zip_base), "zip", root_dir=target_root, base_dir=skill.name)
        artifacts.append(
            {
                "target": target.name,
                "package_type": target.package_kind,
                "skill": skill.name,
                "folder": str(expanded_dir.relative_to(output_dir)),
                "zip": str(Path(archive_path).relative_to(output_dir)),
            }
        )

    return artifacts


def build_codex_plugin(output_dir: Path, target: TargetSpec) -> list[dict[str, str]]:
    target_root = output_dir / target.name
    target_root.mkdir(parents=True, exist_ok=True)

    plugin_dir = target_root / "rootflowai-image"
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)

    shutil.copytree(PLUGIN_ROOT, plugin_dir / ".codex-plugin", dirs_exist_ok=True, ignore=COPY_IGNORE)
    shutil.copytree(SKILLS_ROOT, plugin_dir / "skills", dirs_exist_ok=True, ignore=COPY_IGNORE)
    copy_runtime_scripts(plugin_dir / "scripts")
    copy_file(REPO_ROOT / "README.md", plugin_dir / "README.md")
    copy_file(REPO_ROOT / "LICENSE", plugin_dir / "LICENSE")

    zip_base = target_root / "rootflowai-image-codex-plugin"
    archive_path = shutil.make_archive(str(zip_base), "zip", root_dir=target_root, base_dir="rootflowai-image")

    return [
        {
            "target": target.name,
            "package_type": target.package_kind,
            "skill": "rootflowai-image",
            "folder": str(plugin_dir.relative_to(output_dir)),
            "zip": str(Path(archive_path).relative_to(output_dir)),
        }
    ]


def main() -> int:
    args = parse_args()
    output_dir = (REPO_ROOT / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    artifacts: list[dict[str, str]] = []
    for target in TARGET_SPECS:
        if target.package_kind == "plugin":
            artifacts.extend(build_codex_plugin(output_dir, target))
            continue
        artifacts.extend(build_skill_target(output_dir, target))

    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "output_dir": str(output_dir),
        "artifacts": artifacts,
    }
    (output_dir / "package-index.json").write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(manifest, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
