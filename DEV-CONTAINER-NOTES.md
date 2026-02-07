# Dev Container Notes

Setup notes and gotchas for running Claude Code with `--dangerously-skip-permissions` inside this devcontainer.

## Prerequisites

- **Docker Desktop** must be running on the host
- **VS Code** with the **Dev Containers** extension (`ms-vscode-remote.remote-containers`)
- **`ANTHROPIC_API_KEY`** set as a host environment variable (see Authentication below)

## Building & Opening

Open the Command Palette (`Ctrl+Shift+P`) and run:

```
Dev Containers: Rebuild and Reopen in Container
```

## Authentication

OAuth does not carry into the container. Use an API key instead:

1. Create an API key at https://console.anthropic.com/ (needs the "Claude Code" role)
2. Set it on your host machine:
   ```powershell
   [System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-...', 'User')
   ```
3. Restart VS Code so it picks up the new env var
4. The `containerEnv` entry in `devcontainer.json` forwards it into the container automatically

**Note:** API keys use Console billing (pay-per-token), not Claude.ai subscription billing. Never commit the key to git.

## Gotchas

### Python base image does not include Node.js

The `mcr.microsoft.com/devcontainers/python` image ships without npm/Node.js. Claude Code is an npm package, so Node.js must be added via a dev container feature:

```json
"features": {
  "ghcr.io/devcontainers/features/node:1": {}
}
```

Claude Code is then installed in `postCreateCommand` (not in the Dockerfile) because features are layered *after* the Dockerfile build. This also means `npx` is unavailable during the Dockerfile build — anything that needs Node.js must go in `postCreateCommand`.

### `sudo` cannot find Node.js commands

`sudo` strips the user's PATH due to `secure_path` in sudoers. Commands like `sudo npx ...` or `sudo node ...` will fail with "command not found". Workarounds:

- **Preferred:** Install system dependencies directly via `apt-get` in the Dockerfile (where you're already root)
- If you must use sudo at runtime: `sudo $(which npx) ...` — but this still fails if the command internally calls `node` (which is also not on sudo's PATH)

### `uv sync` fails without `pyproject.toml`

If the project doesn't have a `pyproject.toml` yet, `uv sync` will exit with code 2 and block container setup. The `postCreateCommand` guards against this:

```
if [ -f pyproject.toml ]; then uv sync; fi
```

### `uv run` needed for project-installed CLI tools

Tools installed by `uv sync` (like `playwright`) live in the project's virtual environment, not on the system PATH. Use `uv run <command>` to invoke them:

```
uv run playwright install chromium
```

Plain `playwright install chromium` will fail with "command not found".

### Playwright system deps go in the Dockerfile, browser binary in `postCreateCommand`

Playwright's Chromium needs OS shared libraries (libnss3, libgbm1, etc.) and needs to download a browser binary. These are split across two locations:

- **Dockerfile** — `apt-get install` the shared libraries (runs as root, no Node.js needed)
- **postCreateCommand** — `uv run playwright install chromium` downloads the browser binary (needs the `playwright` Python package installed first via `uv sync`)

You cannot use `npx playwright install-deps` in the Dockerfile because Node.js isn't available yet.

### Playwright must be in `pyproject.toml`

`uv run playwright install chromium` requires `playwright` to be a dependency. Add it as a dev dependency:

```toml
[dependency-groups]
dev = [
    "playwright>=1.49",
    "pytest-playwright>=0.6",
]
```

Without this, `uv sync` won't install it and `uv run playwright` fails with "Failed to spawn".

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
| `Dockerfile` | System packages (iptables, ipset, Playwright libs) and firewall script setup |
| `init-firewall.sh` | Default-deny firewall allowing only whitelisted domains |

## Whitelisted Domains

The firewall allows outbound traffic to:

| Domain | Reason |
|--------|--------|
| `api.anthropic.com` | Claude API |
| `statsig.anthropic.com`, `statsig.com` | Telemetry |
| `sentry.io` | Error reporting |
| `registry.npmjs.org` | npm packages |
| `pypi.org`, `files.pythonhosted.org` | Python packages |
| `playwright.azureedge.net` | Playwright browser downloads |
| `github.com`, `api.github.com` | Git operations, GitHub API |
| `raw.githubusercontent.com`, `objects.githubusercontent.com` | GitHub raw content and git objects |
| `marketplace.visualstudio.com`, `vscode.blob.core.windows.net`, `update.code.visualstudio.com` | VS Code extensions and updates |

Plus all GitHub CIDR ranges from `api.github.com/meta`.
