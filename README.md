# RootFlowAI Image

`rootflowai-image` packages RootFlowAI image workflows for multiple skill hosts, including Codex, Cherry Studio, and Claude-compatible skill runners.
It exposes two explicit billing-lane skills:

- `$rootflowai-image-metered`
- `$rootflowai-image-count`

## What It Includes

- `.codex-plugin/plugin.json`: plugin manifest
- `skills/rootflowai-image-metered/`: metered skill metadata and references
- `skills/rootflowai-image-count/`: count-billed skill metadata and references
- `scripts/generate_image.py`: CLI for image generation
- `scripts/edit_image.py`: CLI for image editing
- `scripts/build_release_packages.py`: multi-platform ZIP builder

## Requirements

- Python 3
- Valid RootFlowAI API key(s)

## Credential Profiles

This repo now supports two billing profiles:

- `metered`: for `gpt-image-2`
- `count`: for `gpt-image-2-count`

Recommended environment variables:

```bash
export ROOTFLOWAI_METERED_API_KEY='your_metered_key'
export ROOTFLOWAI_COUNT_API_KEY='your_count_key'
```

Backward compatibility:

- `ROOTFLOWAI_API_KEY` still works and is treated as the legacy alias for the `metered` profile.

How routing works:

- `--profile auto` is the default
- `gpt-image-2` automatically uses the `metered` profile
- `gpt-image-2-count` automatically uses the `count` profile
- you can override routing explicitly with `--profile metered` or `--profile count`

## Distribution Targets

The repository now supports one source tree with multiple installable package targets:

- `codex-plugin`: full Codex plugin ZIP with `.codex-plugin/`, `skills/`, and root scripts
- `codex-skill`: standalone self-contained skill ZIPs for Codex skill import flows
- `cherry-studio`: standalone self-contained skill ZIPs for Cherry Studio "Install from ZIP"
- `claude-compatible`: standalone self-contained skill ZIPs for `.claude/skills` based hosts

## GitHub Releases

Users do not need to build ZIPs manually if you publish GitHub Releases for the repo.

This repository now includes a release workflow that:

- runs on tag push for tags like `v0.2.0`
- can also be triggered manually from GitHub Actions
- rebuilds every installable package
- uploads all ZIPs plus `package-index.json` to the GitHub Release page

Typical maintainer flow:

```bash
git tag v0.2.0
git push origin v0.2.0
```

After the workflow finishes, users can download the correct installer directly from the Releases page instead of building locally.

Recommended assets for end users:

- Cherry Studio: `rootflowai-image-*-cherry-studio.zip`
- Codex Skill import: `rootflowai-image-*-codex-skill.zip`
- Codex Plugin import: `rootflowai-image-codex-plugin.zip`
- Claude-compatible hosts: `rootflowai-image-*-claude-compatible.zip`

Build all packages locally:

```bash
python3 scripts/build_release_packages.py --output-dir dist
```

Generated artifacts:

- `dist/codex-plugin/rootflowai-image-codex-plugin.zip`
- `dist/codex-skill/rootflowai-image-metered-codex-skill.zip`
- `dist/codex-skill/rootflowai-image-count-codex-skill.zip`
- `dist/cherry-studio/rootflowai-image-metered-cherry-studio.zip`
- `dist/cherry-studio/rootflowai-image-count-cherry-studio.zip`
- `dist/claude-compatible/rootflowai-image-metered-claude-compatible.zip`
- `dist/claude-compatible/rootflowai-image-count-claude-compatible.zip`

The builder also creates expanded folders under `dist/` so you can install from a directory instead of a ZIP when a host supports both.

## Codexapp Skills

Use the explicit skill name that matches the billing lane you want:

- `$rootflowai-image-metered`: standard `gpt-image-2` workflow
- `$rootflowai-image-count`: `gpt-image-2-count` workflow

Examples:

```text
Use $rootflowai-image-metered to generate a new product image and save it to ./out
```

```text
Use $rootflowai-image-count to edit this portrait and save it to ./out
```

## Install By Host

### Codex Plugin

Import `dist/codex-plugin/rootflowai-image-codex-plugin.zip` into a Codex-compatible plugin flow, or install the repository directly as a plugin checkout.

### Codex Skill

Install one of the ZIPs in `dist/codex-skill/`, or point Codex at the expanded folder in that same directory.

### Cherry Studio

Open Cherry Studio `Skills`, choose `Install from ZIP file`, and select one of:

- `dist/cherry-studio/rootflowai-image-metered-cherry-studio.zip`
- `dist/cherry-studio/rootflowai-image-count-cherry-studio.zip`

If you prefer `Install from directory`, select the matching expanded folder under `dist/cherry-studio/`.

### Claude-Compatible Hosts

Use one of the ZIPs in `dist/claude-compatible/`, or unzip/copy the corresponding skill folder into a host-managed `.claude/skills/` directory.

## Quick Start

Set your API key(s):

```bash
export ROOTFLOWAI_METERED_API_KEY='your_metered_key_here'
export ROOTFLOWAI_COUNT_API_KEY='your_count_key_here'
```

Generate an image with the metered model:

```bash
python3 scripts/generate_image.py \
  --prompt 'Three oath brothers doing a short-video livestream' \
  --output-dir ./out
```

Generate an image with the count-billed model:

```bash
python3 scripts/generate_image.py \
  --model gpt-image-2-count \
  --prompt 'Three oath brothers doing a short-video livestream' \
  --output-dir ./out
```

Edit an existing image:

```bash
python3 scripts/edit_image.py \
  --image /absolute/path/to/portrait.jpg \
  --prompt 'Convert this into an American-style professional corporate headshot' \
  --output-dir ./out
```

## Common Options

```bash
python3 scripts/generate_image.py \
  --prompt 'American-style professional headshot, blue studio background' \
  --size 1536x1024 \
  --quality high \
  --n 2 \
  --output-dir ./out \
  --response-path ./out/response.json
```

```bash
python3 scripts/generate_image.py \
  --profile count \
  --prompt 'Minimal product ad shot on a clean studio set' \
  --output-dir ./out
```

```bash
python3 scripts/edit_image.py \
  --image /absolute/path/to/portrait.jpg \
  --profile count \
  --mask /absolute/path/to/mask.png \
  --prompt 'Replace the background with a blue textured studio backdrop' \
  --size 1536x1024 \
  --quality high \
  --output-dir ./out \
  --response-path ./out/edit-response.json
```

## Files

- Skill entrypoints:
  `skills/rootflowai-image-metered/SKILL.md`
  `skills/rootflowai-image-count/SKILL.md`
- Scripts: `scripts/generate_image.py`, `scripts/edit_image.py`
- Packager: `scripts/build_release_packages.py`

## Testing

Run the local test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Validate the release package builder:

```bash
python3 scripts/build_release_packages.py --output-dir dist
```

GitHub Actions also runs the same tests on every push and pull request.

## Notes

- Do not commit API keys into this repository.
- The scripts use Python standard library modules only.
- Source skills keep their canonical runtime in the repository-level `scripts/` directory; release bundles copy those files into each packaged skill so installers get a self-contained artifact.
- Both scripts print `profile_resolved` and `api_key_source` in their JSON output so you can see which billing path was actually used.
- Remote image downloads are restricted to public `https://` URLs to reduce SSRF-style risk when an upstream API returns image links.
- The edit flow in this repo is implemented against the OpenAI-compatible `POST /v1/images/edits` contract. It has not been live-tested against RootFlowAI with a real key and image inside this repo automation session.
