# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`image-describe` is a Python CLI tool that calls Vision API through OpenAI-compatible protocol to identify and describe image content. Defaults to Alibaba Cloud DashScope, supports switching to any compatible API provider.

## Commands

```bash
# Install (development mode)
pip install -e .

# Usage
image-describe <image> [-p <prompt>] [-m <model>]
image-describe capture [-o <path>] [-w <id> | --window-name <name>] [-d] [-p <prompt>] [-m <model>]
image-describe list-windows
image-describe config [--api-key <key>] [--model <model>] [--base-url <url>] [--show]
```

No lint, test suite, or build steps.

## Architecture

```
image_describe/
├── cli.py         # CLI entry, manual sys.argv dispatch to 4 subcommands
├── config.py      # Config read/write at ~/.config/image-describe/config.json (0600)
├── vision.py      # Core: Vision API calls via openai SDK
├── capture.py     # Screenshot module (mss cross-platform + macOS screencapture)
└── window_list.py # macOS window listing (Quartz CGWindowListCopyWindowInfo)
```

- **vision.py** — All API calls through `describe_image()` and `describe_image_data()` (bytes). Local images are base64-encoded to data URLs.
- **config.py** — `load_config()` / `save_config()` manage `~/.config/image-describe/config.json`. Keys: `api_key`, `model`, `base_url`. API Key masked via `mask_key()` (first 6 + last 4 chars). Default base_url: `https://dashscope.aliyuncs.com/compatible-mode/v1`.
- **cli.py** — Manual sys.argv dispatch to four subcommands: `describe`, `capture`, `list-windows`, `config`.
- **capture.py** — `capture_bytes()` returns PNG bytes in memory (mss.grab + to_png, or screencapture to temp file or mss). `capture()` wraps it and saves to file. On macOS with window_id/--window-name, uses `screencapture -l` for occluded-window capture.
- **window_list.py** — macOS only. `list_windows()` lists all visible windows via Quartz. `find_window(name)` does case-insensitive substring matching on window title and owner name.
- **capture flow when `-d` without `-o`**: screenshot → PNG bytes in memory → base64 data URL → Vision API, no file on disk.
- Default model: `qwen3.6-plus`
- `setup.py` registers console_scripts entry point `image-describe`, depends on `openai>=1.0` + `mss`
