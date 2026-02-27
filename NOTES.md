## Server Access

- **URL:** https://ubuntu-2gb-ash-1.tail865b93.ts.net/
- **Hosting:** Hetzner VPS
- **Access requires:** Tailscale VPN connection

## Ideas

Can I cache data locally and only sync intermittently?


[Service]
User=nexus
Group=nexus
WorkingDirectory=/opt/nexus
EnvironmentFile=/opt/nexus/.env
ExecStart=/opt/nexus/.venv/bin/gunicorn nexus.wsgi:application --bind 127.0.0.1:8000 --workers 2
Restart=on-failure
RestartSec=5
