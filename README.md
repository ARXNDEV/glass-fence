# 🛡️ Glass Fence

**AI-Powered Remote Browser Isolation (RBI) Platform**

Built by [ARXNDEV](https://github.com/ARXNDEV)

Glass Fence isolates web browsing in a secure Docker container, streaming only pixels to the user via WebRTC. No web content ever reaches the end-user's device.

## Features
- 🔒 Complete browser isolation — zero content reaches local device
- 🌐 WebRTC pixel streaming — ultra-low latency
- 🤖 AI threat intelligence layer (LangGraph + XGBoost + BERT)
- 👥 Multi-user session support
- 🖥️ Multiple browser profiles — Firefox, Chromium, Chrome, Brave, Edge
- 📊 Real-time threat monitoring dashboard

## Quick Start
```bash
cp .env.example .env
# Edit .env with your passwords and server IP
docker compose up -d
# Visit http://localhost:8081
```

## Architecture
```
User Browser → [Nginx] → [Glass Fence Container] → WebRTC Stream
                              ↕
                    [AI Threat Engine - FastAPI]
                              ↕
                    [LangGraph + XGBoost + BERT]
```

## Environment Variables
| Variable | Description | Default |
|---|---|---|
| GF_USER_PASSWORD | Password for users | changeme |
| GF_ADMIN_PASSWORD | Password for admins | changeme_admin |
| SERVER_PUBLIC_IP | Your server's public IP | 127.0.0.1 |
| VIDEO_CODEC | WebRTC video codec (vp8/vp9/h264) | vp9 |
| SCREEN_RESOLUTION | Virtual desktop resolution | 1920x1080@60 |

## Stack
- **Frontend**: Vue 2 + TypeScript + SCSS
- **Backend**: Go + WebRTC (pion) + WebSocket
- **Streaming**: WebRTC with VP9
- **Infrastructure**: Docker + Nginx + Traefik (prod)

## Built on
Glass Fence is built on top of [n.eko](https://github.com/m1k1o/neko) (Apache 2.0), extended with AI-powered threat intelligence.

## License
Apache 2.0 — © 2025 ARXNDEV
