# SuperSecret

**Stupid-simple, zero-leak secret management with unprecedented automation.**

No more typing secrets into terminals. No more secrets in history, process lists, or environment variables.  
One master password. Encrypted at rest. Auto-injection. Ghost clipboard. Self-destruct.

## Features

- Invisible input (getpass)
- Strong encryption (scrypt + stream cipher, pure Python, zero deps)
- Automatic high-entropy detection & vaulting
- Context-aware injection for common tools
- Clipboard that self-clears
- Shell integration (bash/zsh)
- Zero external dependencies for core crypto

## Quick Install

```bash
curl -sL https://raw.githubusercontent.com/Garrettc123/supersecret/main/install.sh | bash
```

Or clone and run:

```bash
git clone https://github.com/Garrettc123/supersecret.git
cd supersecret
./install.sh
```

## Usage

```bash
secret set <name>          # store a secret (invisible input)
secret get <name>          # copy to clipboard (auto-clears in 30s)
secret list                # list vaulted names
secret rm <name>           # delete
secret watch               # start background agent
secret auto on|off         # enable/disable zero-touch mode
secret status              # live status
```

## Security Model

- Secrets never appear in argv, environment, or shell history
- Encrypted with master password derived via scrypt (N=2^14)
- Files stored as `~/.secrets/*.sec` with mode 600
- Memory is zeroed after use where possible
- Clipboard auto-clears after 30 seconds

## License

MIT — do whatever you want. Just don’t be stupid with your secrets.
