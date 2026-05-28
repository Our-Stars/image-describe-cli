import json
import os
import stat

CONFIG_DIR = os.path.expanduser("~/.config/image-describe")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DEFAULT_MODEL = "qwen3.6-plus"
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def ensure_config_dir():
    """Ensure config directory exists with proper permissions."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, mode=0o700)


def load_config():
    """Load config from file. Returns dict with defaults if not exists."""
    if not os.path.exists(CONFIG_FILE):
        return {"api_key": "", "model": DEFAULT_MODEL, "base_url": DEFAULT_BASE_URL}
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    config.setdefault("api_key", "")
    config.setdefault("model", DEFAULT_MODEL)
    config.setdefault("base_url", DEFAULT_BASE_URL)
    return config


def save_config(config):
    """Save config dict to file with restrictive permissions."""
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)


def get_api_key():
    """Get API key. Raises SystemExit if not configured."""
    config = load_config()
    key = config.get("api_key", "")
    if not key:
        print("错误：未配置 API Key。请运行：")
        print("  image-describe config --api-key <你的API Key>")
        raise SystemExit(1)
    return key


def get_model():
    return load_config().get("model", DEFAULT_MODEL)


def get_base_url():
    return load_config().get("base_url", DEFAULT_BASE_URL)


def mask_key(key):
    """Mask API key: show first 6 and last 4 chars."""
    if len(key) <= 10:
        return "*" * len(key)
    return key[:6] + "*" * (len(key) - 10) + key[-4:]
