# Dev Container Notes

Setup notes and gotchas for running Claude Code with `--dangerously-skip-permissions` inside this devcontainer.

## Prerequisites

- **Docker Desktop** must be running on the host
- **VS Code** with the **Dev Containers** extension (`ms-vscode-remote.remote-containers`)

## Building & Opening

Open the Command Palette (`Ctrl+Shift+P`) and run:

```
Dev Containers: Rebuild and Reopen in Container
```

## Gotchas

### Python base image does not include Node.js

The `mcr.microsoft.com/devcontainers/python` image ships without npm/Node.js. Claude Code is an npm package, so Node.js must be added via a dev container feature:

```json
"features": {
  "ghcr.io/devcontainers/features/node:1": {}
}
```

Claude Code is then installed in `postCreateCommand` (not in the Dockerfile) because features are layered *after* the Dockerfile build.

### `uv sync` fails without `pyproject.toml`

If the project doesn't have a `pyproject.toml` yet, `uv sync` will exit with code 2 and block container setup. The `postCreateCommand` guards against this:

```
if [ -f pyproject.toml ]; then uv sync; fi
```

### Firewall must resolve IPs before locking down

The `init-firewall.sh` script uses a default-deny iptables policy. DNS resolution and the GitHub meta API fetch must happen **before** setting policies to DROP, otherwise the script can't reach the internet to build its own allowlist.

The script is split into two phases:
1. **Phase 1** — Resolve all domain IPs and fetch GitHub CIDR ranges (network is open)
2. **Phase 2** — Flush rules, set DROP policies, add allowlist rules

### GitHub marketplace clone requires HTTPS, not SSH

Inside the container there are no SSH keys configured for GitHub. The marketplace add command must use an HTTPS URL:

```
claude plugin marketplace add https://github.com/anthropics/claude-code.git
```

Using the shorthand `anthropics/claude-code` defaults to SSH and fails with `Permission denied (publickey)`.

### `NET_ADMIN` and `NET_RAW` capabilities are required

The container needs these Docker capabilities for iptables to work:

```json
"runArgs": [
  "--cap-add=NET_ADMIN",
  "--cap-add=NET_RAW"
]
```

Without them, `init-firewall.sh` will fail silently or error on iptables commands.

### Line endings on Windows

If `init-firewall.sh` is saved with CRLF line endings, the `#!/usr/bin/env bash` shebang breaks inside the Linux container. Ensure the file uses LF line endings. Add to `.gitattributes` if needed:

```
*.sh text eol=lf
```

### Firewall DNS resolution is point-in-time

The firewall resolves domain IPs once at container start. If a service (e.g., GitHub, Anthropic) rotates IPs after that, connections may fail. Fix by restarting the container or re-running:

```bash
sudo /usr/local/bin/init-firewall.sh
```

## File Overview

| File | Purpose |
|------|---------|
| `devcontainer.json` | Container config, features, env vars, lifecycle commands |
| `Dockerfile` | System packages (iptables, ipset, etc.) and firewall script setup |
| `init-firewall.sh` | Default-deny firewall allowing only whitelisted domains |

## Whitelisted Domains

The firewall allows outbound traffic to:

| Domain | Reason |
|--------|--------|
| `api.anthropic.com` | Claude API |
| `statsig.anthropic.com`, `statsig.com` | Telemetry |
| `sentry.io` | Error reporting |
| `registry.npmjs.org` | npm packages |
| `github.com`, `api.github.com` | Git operations, GitHub API |
| `raw.githubusercontent.com`, `objects.githubusercontent.com` | GitHub raw content and git objects |
| `marketplace.visualstudio.com`, `vscode.blob.core.windows.net`, `update.code.visualstudio.com` | VS Code extensions and updates |

Plus all GitHub CIDR ranges from `api.github.com/meta`.
