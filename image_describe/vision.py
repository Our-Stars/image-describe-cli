import base64
import os
import sys

from openai import OpenAI


def get_mime_type(path):
    ext = os.path.splitext(path)[1].lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    if ext not in mime_map:
        print(f"Error: unsupported image format '{ext}'. Supported: {list(mime_map.keys())}")
        raise SystemExit(1)
    return mime_map[ext]


def encode_local_image(path):
    if not os.path.exists(path):
        print(f"Error: file not found - {path}")
        raise SystemExit(1)
    mime = get_mime_type(path)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def _call_api(data_url, prompt, api_key, model, base_url):
    client = OpenAI(api_key=api_key, base_url=base_url)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": data_url}},
                    {"type": "text", "text": prompt},
                ],
            },
        ],
    )
    return completion.choices[0].message.content


def describe_image(image_path, prompt, api_key, model, base_url):
    data_url = encode_local_image(image_path)
    return _call_api(data_url, prompt, api_key, model, base_url)


def describe_image_data(image_bytes, prompt, api_key, model, base_url):
    """Describe raw PNG bytes directly, without writing to disk."""
    data_url = f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
    return _call_api(data_url, prompt, api_key, model, base_url)
