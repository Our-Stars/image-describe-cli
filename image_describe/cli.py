import argparse
import sys

from .capture import capture as do_capture
from .capture import capture_bytes as do_capture_bytes
from .config import (
    DEFAULT_MODEL,
    get_api_key,
    get_base_url,
    get_model,
    load_config,
    mask_key,
    save_config,
)
from .vision import describe_image, describe_image_data
from .window_list import find_window as do_find_window
from .window_list import list_windows as do_list_windows


def cmd_describe(args):
    api_key = get_api_key()
    model = args.model or get_model()
    base_url = get_base_url()
    prompt = args.prompt or "Please describe this image in detail."

    try:
        result = describe_image(args.image, prompt, api_key, model, base_url)
        print(result)
    except Exception as e:
        print(f"Error: API call failed - {e}", file=sys.stderr)
        raise SystemExit(1)


def cmd_config(args):
    config = load_config()
    changed = False

    if args.api_key is not None:
        config["api_key"] = args.api_key
        changed = True
        print("API Key updated.")

    if args.model is not None:
        config["model"] = args.model
        changed = True
        print(f"Model updated to: {args.model}")

    if args.base_url is not None:
        config["base_url"] = args.base_url
        changed = True
        print(f"Base URL updated to: {args.base_url}")

    if changed:
        save_config(config)

    if args.show or not changed:
        if config["api_key"]:
            print(f"API Key : {mask_key(config['api_key'])}")
        else:
            print("API Key : (not set)")
        print(f"Model   : {config['model']}")
        print(f"Base URL: {config.get('base_url', '')}")


def _get_describe_args(args):
    return (
        get_api_key(),
        args.model or get_model(),
        get_base_url(),
        args.prompt or "Please describe this image in detail.",
    )


def _resolve_window_id(args):
    """Resolve --window-name to a window ID. Returns the effective window_id."""
    if args.window_name is not None:
        if sys.platform != "darwin":
            print(
                "Warning: --window-name is macOS only, ignored.",
                file=sys.stderr,
            )
            return None
        win = do_find_window(args.window_name)
        return win["id"]
    return args.window_id


def cmd_capture(args):
    window_id = _resolve_window_id(args)

    if args.describe and not args.output:
        try:
            image_bytes = do_capture_bytes(window_id=window_id)
        except Exception as e:
            print(f"Error: screenshot failed - {e}", file=sys.stderr)
            raise SystemExit(1)

        api_key, model, base_url, prompt = _get_describe_args(args)
        try:
            result = describe_image_data(image_bytes, prompt, api_key, model, base_url)
            print(result)
        except Exception as e:
            print(f"Error: API call failed - {e}", file=sys.stderr)
            raise SystemExit(1)
    else:
        try:
            filepath = do_capture(output_path=args.output, window_id=window_id)
            print(f"Screenshot saved: {filepath}")
        except Exception as e:
            print(f"Error: screenshot failed - {e}", file=sys.stderr)
            raise SystemExit(1)

        if args.describe:
            api_key, model, base_url, prompt = _get_describe_args(args)
            try:
                result = describe_image(filepath, prompt, api_key, model, base_url)
                print(result)
            except Exception as e:
                print(f"Error: API call failed - {e}", file=sys.stderr)
                raise SystemExit(1)


def cmd_list_windows(_args):
    windows = do_list_windows()
    for w in windows:
        print(f"{w['id']}\t{w['owner']}\t{w['name']}")


_FMT = argparse.RawDescriptionHelpFormatter


def build_describe_parser():
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=_FMT,
        description="Describe a local image file using Vision API. Supports PNG / JPG / GIF / WebP.",
        epilog=(
            "Examples:\n"
            "  image-describe <image>\n"
            "  image-describe <image> -p <prompt>\n"
            "  image-describe <image> -m <model>"
        ),
    )
    parser.add_argument("image", help="path to local image file")
    parser.add_argument("-p", "--prompt", help="custom prompt for the vision model")
    parser.add_argument(
        "-m", "--model", help=f"model to use (default: %(default)s)", default=DEFAULT_MODEL
    )
    return parser


def build_config_parser():
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=_FMT,
        description=(
            "Manage image-describe configuration.\n"
            "Config file: ~/.config/image-describe/config.json"
        ),
        epilog=(
            "Defaults:\n"
            f"  Model   : {DEFAULT_MODEL}\n"
            "  Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1\n"
            "\n"
            "Examples:\n"
            "  image-describe config --api-key <key>\n"
            "  image-describe config --model <model>\n"
            "  image-describe config --base-url <url>\n"
            "  image-describe config --show"
        ),
    )
    parser.add_argument(
        "--api-key",
        help="set API key (any OpenAI-compatible provider)",
    )
    parser.add_argument(
        "--model",
        help=f"set default model (current: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--base-url",
        help="set API base URL (for switching providers)",
    )
    parser.add_argument(
        "--show", action="store_true", help="show current configuration"
    )
    return parser


def build_capture_parser():
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=_FMT,
        description=(
            "Capture the screen, optionally call Vision API to describe it.\n"
            "\n"
            "On macOS, use --window-name to auto-detect and capture a specific window\n"
            "by its title (case-insensitive substring match). The window is captured even\n"
            "if occluded by others (deep window capture).\n"
            "Use -w to capture by window ID directly.\n"
            "On other platforms, a full-screen screenshot is taken and window options are ignored.\n"
            "\n"
            "Screenshots are saved to ~/.config/image-describe/captures/ by default.\n"
            "When using -d without -o, the screenshot is processed in-memory and not\n"
            "written to disk."
        ),
        epilog=(
            "Examples:\n"
            "  image-describe capture                                # full screen, save to default dir\n"
            "  image-describe capture -o <path>                      # save to a specific path\n"
            "  image-describe capture -d                             # capture and describe, no file saved\n"
            "  image-describe capture -d -o <path>                   # capture, save and describe\n"
            "  image-describe capture -d -p <prompt>                 # custom describe prompt\n"
            "  image-describe capture -w <window-id> -d              # macOS: capture by window ID\n"
            "  image-describe capture --window-name <name> -d        # macOS: capture by window name"
        ),
    )
    parser.add_argument(
        "-o", "--output",
        help="output path (default: ~/.config/image-describe/captures/screenshot_<timestamp>.png)",
    )
    window_group = parser.add_mutually_exclusive_group()
    window_group.add_argument(
        "-w", "--window-id",
        type=int,
        help="target window ID (macOS only)",
    )
    window_group.add_argument(
        "--window-name",
        help="target window name — case-insensitive substring match (macOS only)",
    )
    parser.add_argument(
        "-d", "--describe",
        action="store_true",
        help="call Vision API to describe the screenshot",
    )
    parser.add_argument(
        "-p", "--prompt",
        help="custom prompt (used with -d)",
    )
    parser.add_argument(
        "-m", "--model",
        help="model to use for describing",
    )
    return parser


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "image-describe — Describe images using Vision API\n"
            "\n"
            "Usage:\n"
            "  image-describe describe   <image>  [-p <prompt>] [-m <model>]\n"
            "  image-describe capture    [-o <path>] [-w <id> | --window-name <name>] [-d] [-p <prompt>] [-m <model>]\n"
            "  image-describe list-windows\n"
            "  image-describe config     [--api-key <key>] [--model <model>] [--base-url <url>] [--show]\n"
            "\n"
            "Subcommands:\n"
            "  describe        describe a local image file\n"
            "  capture         capture the screen and optionally describe it\n"
            "  list-windows    list visible macOS windows (for use with capture -w)\n"
            "  config          manage API key / model / base URL settings\n"
            "\n"
            "Run \"image-describe <subcommand> --help\" for detailed help on each subcommand."
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
    elif subcommand == "capture":
        if len(sys.argv) > 2 and sys.argv[2] in ("-h", "--help"):
            build_capture_parser().print_help()
            raise SystemExit(0)
        parser = build_capture_parser()
        args = parser.parse_args(sys.argv[2:])
        cmd_capture(args)
    elif subcommand == "list-windows":
        if len(sys.argv) > 2 and sys.argv[2] in ("-h", "--help"):
            print(
                "List all visible macOS windows, output as tab-separated \"window-id\\tapp\\ttitle\".\n"
                "\n"
                "This command is macOS only. The output format is designed for easy parsing\n"
                "by LLMs or scripts, to be used with capture -w <window-id>.\n"
                "\n"
                "Usage:\n"
                "  image-describe list-windows\n"
                "\n"
                "Example output:\n"
                "  95727   PetBuddy        PetBuddy\n"
                "  104384  Terminal        ~ — zsh"
            )
            raise SystemExit(0)
        cmd_list_windows(None)
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
