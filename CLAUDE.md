# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

`image-describe` 是一个 Python CLI 工具，通过 OpenAI 兼容协议调用 Vision API 识别和描述图片内容。默认使用阿里云 DashScope，支持切换到任意兼容的 API 厂商。

## 开发命令

```bash
# 安装（开发模式）
pip install -e .

# 使用
image-describe <图片路径>                    # 描述本地图片
image-describe <图片路径> -p "自定义prompt"   # 自定义 prompt
image-describe <图片路径> -m <模型名>         # 指定模型
image-describe capture                      # 全屏截图（macOS 可指定窗口）
image-describe capture -w <窗口ID>           # macOS 穿透遮挡截取指定窗口
image-describe capture -d                   # 截图并描述
image-describe list-windows                 # macOS 列出所有窗口（供大模型选 ID）
image-describe config --api-key <key>        # 设置 API Key
image-describe config --base-url <url>       # 设置 Base URL（切换厂商）
image-describe config --show                 # 查看当前配置
```

没有 lint、测试套件或构建步骤。

## 架构

```
image_describe/
├── cli.py         # CLI 入口，argparse 子命令分发（describe + capture + list-windows + config）
├── config.py      # 配置读写，存储在 ~/.config/image-describe/config.json，权限 0600
├── vision.py      # 核心：通过 openai SDK 调用 Vision API
├── capture.py     # 截图模块（mss 跨平台全屏 + macOS screencapture 窗口深度截图）
└── window_list.py # macOS 窗口列表（Quartz CGWindowListCopyWindowInfo）
```

- **vision.py** — 所有 API 调用都通过 `describe_image()` 函数。本地图片 base64 编码为 data URL 后发送。
- **config.py** — `load_config()` / `save_config()` 管理 `~/.config/image-describe/config.json`。配置项：`api_key`、`model`、`base_url`。API Key 通过 `mask_key()` 实现部分脱敏显示（显示前6后4位）。默认 base_url 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。
- **cli.py** — 手工解析 sys.argv 分发到四个子命令。新增 `capture`（截图+可选的描述）和 `list-windows`（macOS 窗口列表）。
- **capture.py** — `capture()` 统一截图入口。macOS 上指定 window_id 时调 `screencapture -l` 穿透遮挡截指定窗口，否则用 `mss` 截全屏。
- **window_list.py** — macOS 专用，`list_windows()` 通过 Quartz 框架列出所有可见窗口（ID + 应用名 + 窗口标题），供大模型或人类选择目标窗口。
- 默认模型：`qwen3.6-plus`
- `setup.py` 注册 console_scripts 入口点 `image-describe`，依赖 `openai>=1.0` + `mss`
