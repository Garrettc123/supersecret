"""
Vault operations – encrypted storage under ~/.secrets
"""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Optional

from crypto import encrypt, decrypt

STORE = Path.home() / ".secrets"
STORE.mkdir(mode=0o700, exist_ok=True)
CONFIG_PATH = STORE / "config.json"


def _sec_path(name: str) -> Path:
    # Sanitize name
    safe = "".join(c for c in name if c.isalnum() or c in "-_.")
    if not safe:
        raise ValueError("Invalid secret name")
    return STORE / f"{safe}.sec"


def store(name: str, secret: str, master: str) -> None:
    path = _sec_path(name)
    blob = encrypt(secret.encode("utf-8"), master)
    path.write_bytes(blob)
    path.chmod(0o600)


def load(name: str, master: str) -> str:
    path = _sec_path(name)
    if not path.exists():
        raise FileNotFoundError(f"No secret named '{name}'")
    blob = path.read_bytes()
    plaintext = decrypt(blob, master)
    return plaintext.decode("utf-8")


def delete(name: str) -> bool:
    path = _sec_path(name)
    if path.exists():
        path.unlink()
        return True
    return False


def list_names() -> list[str]:
    return sorted(p.stem for p in STORE.glob("*.sec"))


def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {
        "auto": False,
        "clipboard_ttl": 30,
        "agent": False,
    }


def save_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
    CONFIG_PATH.chmod(0o600)
