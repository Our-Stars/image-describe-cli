# image-describe 🖼️

[English](README.md) | 中文

一个通过 OpenAI 兼容协议调用 Vision API 识别和描述图片内容的命令行工具。默认使用阿里云 DashScope，支持切换到任意兼容的 API 厂商。

## 安装

```bash
pip install image-describe
```

或从源码安装：

```bash
pip install -e .
```

## 使用方法

### 配置 API Key

在你使用的厂商处获取 API Key（如 [DashScope](https://dashscope.aliyun.com/)、[OpenAI](https://platform.openai.com/)），然后配置：

```bash
image-describe config --api-key <你的API-Key>
```

### 识别图片

```bash
image-describe photo.jpg
image-describe photo.jpg -p "这张图片里有什么物体？"
image-describe photo.jpg -m qwen-vl-max
```

### 切换厂商

```bash
image-describe config --base-url https://api.openai.com/v1
```

### 管理配置

```bash
image-describe config --show            # 查看当前配置
image-describe config --model <模型>    # 修改默认模型
image-describe config --api-key <key>   # 更新 API Key
image-describe config --base-url <url>  # 修改 API 端点
```

## 支持的格式

PNG、JPEG、GIF、WebP。

## 环境要求

- Python 3.8+
- `openai >= 1.0`

## 工作原理

本工具通过 OpenAI 兼容接口调用 Vision 模型，图片以 base64 编码后内联发送。
