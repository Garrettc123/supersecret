"""
Ghost clipboard – write then auto-clear
"""

from __future__ import annotations
import subprocess
import time
from typing import Optional


def _run(cmd: list[str], data: bytes = b"") -> bool:
    try:
        subprocess.run(cmd, input=data, check=True, capture_output=True, timeout=2)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False


def copy(text: str) -> bool:
    data = text.encode("utf-8")
    candidates = [
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
        ["pbcopy"],
        ["wl-copy"],
    ]
    for cmd in candidates:
        if _run(cmd, data):
            return True
    return False


def clear() -> None:
    candidates = [
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
        ["pbcopy"],
        ["wl-copy"],
    ]
    for cmd in candidates:
        if _run(cmd, b""):
            return


def ghost_copy(text: str, ttl: int = 30) -> bool:
    """Copy then schedule clear. Returns True if copy succeeded."""
    if not copy(text):
        return False
    # Best-effort zero
    text = "\0" * len(text)
    time.sleep(ttl)
    clear()
    return True
