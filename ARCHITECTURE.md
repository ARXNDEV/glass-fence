# Glass Fence System Architecture

Glass Fence is an AI-Powered Remote Browser Isolation (RBI) system designed to secure enterprise endpoints from web-borne threats. It runs fully containerized browsing environments using WebRTC, ensuring no malicious code ever reaches the user's actual machine.

## High-Level Architecture

Glass Fence is composed of three primary components:

1. **The Go WebRTC Server (`/server`)**: A robust backend written in Go that interfaces with X11 and GStreamer. It captures the screen and audio from the containerized X-server and streams it over WebRTC to the client. It also receives mouse and keyboard input from the client and injects it into the container via `xdotool` or direct X11 commands.
2. **The Vue.js Frontend (`/client`)**: A modern, responsive single-page application built with Vue.js and TypeScript. It uses native WebRTC APIs to receive the video/audio streams and captures user input events to send back to the server over WebRTC DataChannels.
3. **The Docker Images (`/apps`)**: Each browser environment (Firefox, Chromium, XFCE desktop) is packaged as a lightweight Docker container based on a common Ubuntu base image.

## Data Flow

### Video & Audio Streaming
1. An isolated X-server (`Xvfb`) runs headlessly inside the Docker container.
2. Firefox/Chromium is launched inside this X-server.
3. PulseAudio creates a virtual audio sink.
4. The Go server uses GStreamer to capture the X11 screen and PulseAudio sink.
5. GStreamer encodes the raw frames to VP8/H264 video and Opus audio.
6. The Go server's WebRTC engine (`pion/webrtc`) transmits the encoded packets directly to the Vue frontend via UDP.

### Input Handling
1. The Vue frontend captures mouse movements, clicks, and keystrokes on the video element.
2. These events are serialized and sent over a WebRTC DataChannel (TCP-like reliable channel) to the Go server.
3. The Go server deserializes the events and injects them into the X-server.

## Deployment & Production

### Traefik Reverse Proxy
In production, Glass Fence uses Traefik to securely expose the containers to the internet.
Traefik handles:
- Let's Encrypt SSL/TLS generation (required for WebRTC Clipboard/Microphone APIs).
- Subdomain routing (e.g., `firefox.glassfence.local` -> Firefox container).
- Load balancing across multiple instances (if scaled).

### UDP Multiplexing
To avoid the overhead of opening hundreds of UDP ports in Docker, Glass Fence uses WebRTC UDP Multiplexing (`GF_WEBRTC_UDPMUX`). All WebRTC traffic for a specific container is routed through a single UDP port.

## Build System

Glass Fence uses a multi-stage Docker build process managed by GitHub Actions:
1. `base`: Compiles the Vue frontend, compiles the Go backend, and creates the foundational Ubuntu image with X11, PulseAudio, and GStreamer installed.
2. `firefox` / `chromium` / `xfce`: Inherit from `base` and install the specific target application.

To build manually locally, use the `./build` script.
To build for production, push to the `main` branch to trigger the `.github/workflows/docker-build.yml` pipeline.
