# Glass Fence

AI-Powered Remote Browser Isolation (RBI) platform for secure, sandboxed browsing.

Glass Fence provides a highly secure, containerized browser environment that physically isolates web threats from your local network. Powered by real-time AI threat analysis, it delivers unparalleled security for zero-trust architectures.

## Quick Start

```bash
git clone https://github.com/ARXNDEV/glass-fence.git
cd glass-fence
docker-compose -f docker-compose.prod.yaml up -d
```

## Features

- **True Isolation**: Web code executes entirely within an ephemeral container; only a sterile video/audio stream and UI events cross the boundary.
- **AI-Powered Threat Analysis**: Built-in machine learning models actively screen URLs and visual content for phishing, malware, and suspicious behavior.
- **Observability**: Real-time insights and monitoring with comprehensive Prometheus metrics available at `/metrics`, fully integrated with Grafana.
- **High Performance**: Low-latency WebRTC streaming ensures a seamless user experience that feels like a local browser.

## Monitoring & Observability

Glass Fence exports Prometheus metrics at `/metrics`. A complete Grafana dashboard is included in the production deployment to monitor:
- Active sessions and session durations
- WebRTC performance, bitrates, and error rates
- AI Engine screening volume and threat categorizations

*Developed by ARXNDEV.*
