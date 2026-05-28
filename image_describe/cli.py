import argparse
import sys

from .config import (
    DEFAULT_MODEL,
    get_api_key,
    get_base_url,
    get_model,
    load_config,
    mask_key,
    save_config,
)
from .vision import describe_image


def cmd_describe(args):
    api_key = get_api_key()
    model = args.model or get_model()
    base_url = get_base_url()
    prompt = args.prompt or "请详细描述这张图片的内容"

    try:
        result = describe_image(args.image, prompt, api_key, model, base_url)
        print(result)
    except Exception as e:
        print(f"错误：API 调用失败 - {e}", file=sys.stderr)
        raise SystemExit(1)


def cmd_config(args):
    config = load_config()
    changed = False

    if args.api_key is not None:
        config["api_key"] = args.api_key
        changed = True
        print("API Key 已更新。")

    if args.model is not None:
        config["model"] = args.model
        changed = True
        print(f"模型已更新为: {args.model}")

    if args.base_url is not None:
        config["base_url"] = args.base_url
        changed = True
        print(f"Base URL 已更新为: {args.base_url}")

    if changed:
        save_config(config)

    if args.show or not changed:
        if config["api_key"]:
            print(f"API Key : {mask_key(config['api_key'])}")
        else:
            print("API Key : (未设置)")
        print(f"模型    : {config['model']}")
        print(f"Base URL: {config.get('base_url', '')}")


def build_describe_parser():
    """A standalone parser for the describe command (image path + options)."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("image", help="本地图片路径")
    parser.add_argument("-p", "--prompt", help="自定义识别 prompt")
    parser.add_argument("-m", "--model", help=f"指定模型（默认: {DEFAULT_MODEL}）")
    return parser


def build_config_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--api-key", help="设置 DashScope API Key")
    parser.add_argument("--model", help=f"设置默认模型（当前: {DEFAULT_MODEL}）")
    parser.add_argument("--base-url", help="设置兼容 API 的 Base URL")
    parser.add_argument("--show", action="store_true", help="显示当前配置")
    return parser


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "image-describe — 通过 Qwen Vision API 识别图片内容\n"
            "\n"
            "用法:\n"
            "  image-describe <图片路径> [-p <prompt>] [-m <模型>]\n"
            "  image-describe config [--api-key <key>] [--model <模型>] [--base-url <url>] [--show]"
        )
        raise SystemExit(0)

    subcommand = sys.argv[1]

    if subcommand == "config":
        if len(sys.argv) > 2 and sys.argv[2] in ("-h", "--help"):
            build_config_parser().print_help()
            raise SystemExit(0)
        parser = build_config_parser()
        args = parser.parse_args(sys.argv[2:])
        cmd_config(args)
    else:
        remaining = sys.argv[1:]
        if "-h" in remaining or "--help" in remaining:
            build_describe_parser().print_help()
            raise SystemExit(0)
        parser = build_describe_parser()
        args = parser.parse_args(remaining)
        cmd_describe(args)


if __name__ == "__main__":
    main()
