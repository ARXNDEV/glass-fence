# 🛡️ Glass Fence

**Glass Fence** is an AI-Powered Remote Browser Isolation (RBI) system designed to secure enterprise endpoints from web-borne threats. It runs fully containerized browsing environments using WebRTC, ensuring no malicious code ever reaches the local endpoint.

## Features

- **Zero-Trust Browsing**: Execute all web content in an isolated, disposable container.
- **AI-Powered Threat Detection**: Real-time traffic analysis and active threat blocking.
- **Glass Morphism UI**: A premium, visually stunning interface that provides real-time threat telemetry.
- **WebRTC Streaming**: Ultra-low latency, zero-install remote rendering.

## Quick Start

```yaml
version: "3.4"
services:
  glass-fence:
    image: arxndevv/glass-fence:latest
    restart: "unless-stopped"
    shm_size: "2gb"
    ports:
      - "8080:8080"
      - "52000-52100:52000-52100/udp"
    environment:
      NEKO_DESKTOP_SCREEN: 1920x1080@60
      NEKO_MEMBER_MULTIUSER_USER_PASSWORD: user
      NEKO_MEMBER_MULTIUSER_ADMIN_PASSWORD: admin
      NEKO_WEBRTC_EPR: 52000-52100
      NEKO_WEBRTC_NAT1TO1: <your-IP>
```

Run `docker compose up -d` to launch your secure isolation environment.

## Architecture

Glass Fence utilizes GStreamer for rapid screen capture, an internal WebRTC server for streaming, and a Vue.js frontend featuring a custom Glass Morphism UI.

## License

Glass Fence is built upon open-source technologies. Copyright ARXNDEV.
