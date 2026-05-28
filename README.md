# image-describe 🖼️

English | [中文](README_CN.md)

A simple CLI tool to describe images via OpenAI-compatible Vision APIs. Works with DashScope (default), OpenAI, or any compatible provider.

## Installation

```bash
pip install image-describe
```

Or install from source:

```bash
pip install -e .
```

## Usage

### Set up your API Key

Get an API Key from your provider (e.g. [DashScope](https://dashscope.aliyun.com/), [OpenAI](https://platform.openai.com/)), then configure it:

```bash
image-describe config --api-key <your-api-key>
```

### Describe an image

```bash
image-describe photo.jpg
image-describe photo.jpg -p "What objects are in this image?"
image-describe photo.jpg -m qwen-vl-max
```

### Switch providers

```bash
image-describe config --base-url https://api.openai.com/v1
```

### Manage configuration

```bash
image-describe config --show            # Show current settings
image-describe config --model <model>   # Change default model
image-describe config --api-key <key>   # Update API Key
image-describe config --base-url <url>  # Change API endpoint
```

## Supported Formats

PNG, JPEG, GIF, WebP.

## Requirements

- Python 3.8+
- `openai >= 1.0`

## How It Works

This tool calls Vision models through OpenAI-compatible APIs. Images are base64-encoded and sent inline.
