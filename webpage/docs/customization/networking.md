---
sidebar_label: "Networking"
description: "Example networking configurations for Glass Fence."
---

# Networking Customization

## Accessing Glass Fence over the Internet {#internet}

If you want to access Glass Fence over the internet, you need to expose the necessary ports on your router or firewall.

This is the default configuration for Glass Fence so no additional configuration is needed.

## Accessing Glass Fence over a VPN {#vpn}

If you want to access Glass Fence over a VPN, you need to set NAT1TO1 to your server's IP address in the VPN network. This allows Glass Fence to communicate with the server over the VPN.

```yaml title="docker-compose.yaml"
services:
  glass-fence:
    image: "arxndevv/glass-fence/firefox:latest"
    restart: "unless-stopped"
    shm_size: "2gb"
    ports:
      - "8080:8080"
      - "52000-52100:52000-52100/udp"
    environment:
      GF_WEBRTC_EPR: 52000-52100
      GF_WEBRTC_ICELITE: 1
      GF_WEBRTC_NAT1TO1: <your-VPN-IP>
```

## Accessing Glass Fence over SSH {#ssh}

If you do not want to expose Glass Fence to the internet and want to access it securely over SSH, you can set up port forwarding using SSH. This allows you to access Glass Fence from your local machine without exposing it to the internet.

Start glass-fence with TCP multiplexing enabled and NAT1to1 set to loopback address. That way everytime you access Glass Fence, it will use the loopback address to connect to the server.

```yaml title="docker-compose.yaml"
services:
  glass-fence:
    image: "arxndevv/glass-fence/nvidia-firefox:latest"
    restart: "unless-stopped"
    shm_size: "2gb"
    ports:
      - "8080:8080"
      - "52000:52000"
    environment:
      GF_WEBRTC_TCPMUX: 52000
      GF_WEBRTC_ICELITE: 1
      GF_WEBRTC_NAT1TO1: 127.0.0.1
```

Set up your SSH configuration file (`~/.ssh/config`) to include the following port forwarding settings. This will forward the ports from the remote server to your local machine.

```shell title="~/.ssh/config"
Host PC-Work
    HostName work.example.com
    User xxx
    Port xyy
    RemoteForward 8080 localhost:8080
    RemoteForward 52000 localhost:52000
```
