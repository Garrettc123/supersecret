# SuperSecret

**Full implementation – stupid-simple, zero-leak secret management.**

Invisible input. Strong encryption. Ghost clipboard. Auto mode. Background agent.

## Install

```bash
git clone https://github.com/Garrettc123/supersecret.git
cd supersecret
./install.sh
source ~/.bashrc   # or ~/.zshrc
```

## Commands

```bash
secret set <name>       # store (invisible)
secret get <name>       # ghost clipboard (auto-clear)
secret list
secret rm <name>
secret auto on|off
secret watch            # background agent
secret status
```

## Security

- scrypt (N=2^15) key derivation
- Random nonce + SHA-256 stream cipher
- Files mode 600 under ~/.secrets
- No secrets in argv / history / env
- Clipboard self-destructs

## License

MIT
