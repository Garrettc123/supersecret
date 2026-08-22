#!/usr/bin/env bash
set -euo pipefail

echo "→ Installing SuperSecret (full implementation)..."

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_BIN="${HOME}/.local/bin"
INSTALL_LIB="${HOME}/.local/lib/supersecret"
VAULT="${HOME}/.secrets"

mkdir -p "$INSTALL_BIN" "$INSTALL_LIB" "$VAULT"
chmod 700 "$VAULT"

# Install library modules
cp "$ROOT/lib/crypto.py" "$INSTALL_LIB/"
cp "$ROOT/lib/vault.py" "$INSTALL_LIB/"
cp "$ROOT/lib/clipboard.py" "$INSTALL_LIB/"
touch "$INSTALL_LIB/__init__.py"

# Install CLI
cp "$ROOT/bin/secret" "$INSTALL_BIN/secret"
chmod +x "$INSTALL_BIN/secret"

# PATH
SHELL_RC=""
if [[ -n "${ZSH_VERSION:-}" ]]; then
    SHELL_RC="${HOME}/.zshrc"
elif [[ -n "${BASH_VERSION:-}" ]]; then
    SHELL_RC="${HOME}/.bashrc"
else
    SHELL_RC="${HOME}/.profile"
fi

if ! grep -q '\.local/bin' "$SHELL_RC" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    echo "  → Added ~/.local/bin to PATH"
fi

echo ""
echo "✓ SuperSecret full implementation installed."
echo ""
echo "  secret status"
echo "  secret set <name>"
echo "  secret get <name>"
echo ""
echo "Reload: source $SHELL_RC"
