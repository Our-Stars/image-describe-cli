"""macOS window listing module. Lists all visible on-screen windows with their IDs."""
import sys


def list_windows():
    """List all visible on-screen windows. macOS only.

    Returns:
        list[dict]: each window has id, owner, name fields
    """
    if sys.platform != "darwin":
        print("Error: list-windows is only supported on macOS", file=sys.stderr)
        raise SystemExit(1)

    try:
        from Quartz import (  # type: ignore
            CGWindowListCopyWindowInfo,
            kCGNullWindowID,
            kCGWindowListOptionOnScreenOnly,
        )
    except ImportError:
        print("Error: pyobjc-framework-Quartz is required", file=sys.stderr)
        print("Install with: pip install pyobjc-framework-Quartz", file=sys.stderr)
        raise SystemExit(1)

    infos = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly, kCGNullWindowID
    )

    windows = []
    for info in infos:
        name = info.get("kCGWindowName", "")
        if name:
            windows.append(
                {
                    "id": info["kCGWindowNumber"],
                    "owner": info.get("kCGWindowOwnerName", ""),
                    "name": name,
                }
            )

    return windows
