# Glass Fence

**AI-Powered Remote Browser Isolation Platform**

Glass Fence provides secure, isolated browser sessions streamed via WebRTC pixel streams with real-time AI threat intelligence.

## Architecture

```
User Browser → [Traefik TLS] → [Glass Fence Container] → WebRTC Pixel Stream
                                        ↕
                           [AI Threat Engine - FastAPI]
                                        ↕
                         [LangGraph + XGBoost + DistilBERT]
```

## Quick Start

```bash
git clone https://github.com/arxndev/glass-fence.git
cd glass-fence
cp .env.example .env
# Edit .env — set DOMAIN, GF_ADMIN_PASSWORD, GF_USER_PASSWORD, SERVER_PUBLIC_IP
docker compose up -d
```

Access at `http://localhost:8081` (Firefox) or `http://localhost:8082` (Chromium).

## AI Threat Intelligence

Glass Fence includes a three-layer AI threat classifier:

1. **URL Feature Extraction** — Length, entropy, TLD risk scoring, suspicious keyword detection, IP-as-hostname detection
2. **XGBoost Classifier** — Trained on URL feature vectors for phishing/malware detection
3. **DistilBERT Text Classifier** — Deep learning analysis for ambiguous/suspicious URLs

Orchestration via **LangGraph** determines which layers to invoke based on confidence thresholds.

- `POST /screen-url` — Pre-screen a URL before navigation
- `WebSocket /ws/threats` — Real-time threat event feed
- `GET /threats/summary` — Aggregated threat counts by category

## Admin Dashboard

Access the AI Engine admin dashboard at `GET /dashboard` (protected by HTTP Basic Auth).

Shows:
- Threats today / this week
- Category breakdown (safe, suspicious, phishing, malware)
- Last 50 threat events with scores and blocked status
- Auto-refreshes every 30 seconds

## Monitoring

- **Prometheus** — Scrapes metrics from Glass Fence server (`/metrics`) and AI engine (`/metrics`)
- **Grafana** — Pre-configured dashboard at `grafana.${DOMAIN}` with panels for active sessions, session duration, threats/hour, AI latency, stream bitrate

## Services

| Service | Description | Port |
|---------|-------------|------|
| Firefox | Isolated Firefox browser | 8081 |
| Chromium | Isolated Chromium browser | 8082 |
| XFCE Desktop | Full Linux desktop | 8084 |
| AI Engine | Threat intelligence API | 8000 |

## Production Deployment

```bash
docker compose -f docker-compose.prod.yaml up -d
```

Includes:
- Traefik reverse proxy with automatic TLS (Let's Encrypt)
- TURN server (coturn) for NAT traversal
- Rate limiting on all browser services
- Structured JSON logging with rotation
- Automated daily backups with 7-day retention
- Prometheus + Grafana monitoring stack

## Environment Variables

See [.env.example](.env.example) for all available configuration options.

Key variables:
- `GF_ADMIN_PASSWORD` — Admin password (required)
- `GF_USER_PASSWORD` — User password (required)
- `SERVER_PUBLIC_IP` — Server public IP for WebRTC
- `DOMAIN` — Domain for Traefik routing
- `TURN_SERVER` / `TURN_SECRET` — TURN server configuration

## License

See [LICENSE](LICENSE) for details.

*Developed by arxndev.*
