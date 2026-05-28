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


def find_window(name_query):
    """Find a window by name (case-insensitive substring match). macOS only.

    Searches both window title and owner name. Raises SystemExit if zero or
    multiple matches.

    Returns:
        dict: matched window with id, owner, name fields
    """
    windows = list_windows()
    query = name_query.lower()
    matches = [
        w for w in windows
        if query in w["name"].lower() or query in w["owner"].lower()
    ]

    if len(matches) == 0:
        print(
            f"Error: no window matching '{name_query}' found.", file=sys.stderr
        )
        print(
            "Run 'image-describe list-windows' to see available windows.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    if len(matches) == 1:
        return matches[0]

    print(
        f"Error: multiple windows match '{name_query}':", file=sys.stderr
    )
    for w in matches:
        print(f"  {w['id']}\t{w['owner']}\t{w['name']}", file=sys.stderr)
    print("\nUse -w <window-id> to specify one directly.", file=sys.stderr)
    raise SystemExit(1)
