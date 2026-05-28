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
image-describe config --api-key <key>        # 设置 API Key
image-describe config --base-url <url>       # 设置 Base URL（切换厂商）
image-describe config --show                 # 查看当前配置
```

没有 lint、测试套件或构建步骤。

## 架构

```
image_describe/
├── cli.py       # CLI 入口，argparse 子命令分发（describe + config）
├── config.py    # 配置读写，存储在 ~/.config/image-describe/config.json，权限 0600
└── vision.py    # 核心：通过 openai SDK 调用 DashScope Qwen Vision API
```

- **vision.py** — 所有 API 调用都通过 `describe_image()` 函数。本地图片 base64 编码为 data URL 后发送。
- **config.py** — `load_config()` / `save_config()` 管理 `~/.config/image-describe/config.json`。配置项：`api_key`、`model`、`base_url`。API Key 通过 `mask_key()` 实现部分脱敏显示（显示前6后4位）。默认 base_url 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。
- **cli.py** — 默认第一个参数是图片路径（describe 子命令），`config` 子命令管理设置。使用手工解析的 sys.argv 而非标准 argparse subparsers。
- 默认模型：`qwen3.6-plus`
- `setup.py` 注册 console_scripts 入口点 `image-describe`
