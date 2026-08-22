#!/usr/bin/env bash
set -euo pipefail

echo "→ Installing SuperSecret..."

INSTALL_DIR="${HOME}/.local/bin"
mkdir -p "$INSTALL_DIR"

# Copy the secret binary
cp bin/secret "$INSTALL_DIR/secret"
chmod +x "$INSTALL_DIR/secret"

# Ensure PATH
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    SHELL_RC=""
    if [[ -n "${ZSH_VERSION:-}" ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ -n "${BASH_VERSION:-}" ]]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
    echo "  Added $INSTALL_DIR to PATH in $SHELL_RC"
fi

# Create vault
mkdir -p "$HOME/.secrets"
chmod 700 "$HOME/.secrets"

echo ""
echo "✓ SuperSecret installed."
echo ""
echo "Run:  secret status"
echo "Then: secret set my-api-key"
echo ""
echo "Reload your shell or run: source ~/.bashrc  (or ~/.zshrc)"
