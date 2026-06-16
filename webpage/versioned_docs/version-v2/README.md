---
sidebar_position: 2
title: Getting started
---

# Getting started & FAQ

<div align="center">
  <img src="/v2/firefox.svg" title="arxndev/glass-fence:firefox" width="60" height="auto"/>
  <img src="/v2/google-chrome.svg" title="arxndev/glass-fence:google-chrome" width="60" height="auto"/>
  <img src="/v2/chromium.svg" title="arxndev/glass-fence:chromium" width="60" height="auto"/>
  <img src="/v2/microsoft-edge.svg" title="arxndev/glass-fence:microsoft-edge" width="60" height="auto"/>
  <img src="/v2/brave.svg" title="arxndev/glass-fence:brave" width="60" height="auto"/>
  <img src="/v2/vivaldi.svg" title="arxndev/glass-fence:vivaldi" width="60" height="auto"/>
  <img src="/v2/opera.svg" title="arxndev/glass-fence:opera" width="60" height="auto"/>
  <img src="/v2/tor-browser.svg" title="arxndev/glass-fence:tor-browser" width="60" height="auto"/>
  <img src="/v2/remmina.png" title="arxndev/glass-fence:remmina" width="60" height="auto"/>
  <img src="/v2/vlc.svg" title="arxndev/glass-fence:vlc" width="60" height="auto"/>
  <img src="/v2/xfce.svg" title="arxndev/glass-fence:xfce" width="60" height="auto"/>
  <img src="/v2/kde.svg" title="arxndev/glass-fence:kde" width="60" height="auto"/>
</div>

Use the following docker images from [Docker Hub](https://hub.docker.com/r/arxndev/glass-fence) for x86_64:
- `arxndev/glass-fence:latest` or `arxndev/glass-fence:firefox` - for Firefox.
- `arxndev/glass-fence:chromium` - for Chromium.
- `arxndev/glass-fence:google-chrome` - for Google Chrome.
- `arxndev/glass-fence:ungoogled-chromium` - for [Ungoogled Chromium](https://github.com/Eloston/ungoogled-chromium) (by @whalehub).
- `arxndev/glass-fence:microsoft-edge` - for Microsoft Edge.
- `arxndev/glass-fence:brave` - for [Brave Browser](https://brave.com).
- `arxndev/glass-fence:vivaldi` - for [Vivaldi Browser](https://vivaldi.com) (by @Xeddius).
- `arxndev/glass-fence:opera` for [Opera Browser](https://opera.com) (requires extra steps to enable DRM, see instructions [here](https://www.reddit.com/r/operabrowser/wiki/opera/linux_widevine_config/). libffmpeg is already configured.) (by @prophetofxenu)
- `arxndev/glass-fence:tor-browser` - for Tor Browser.
- `arxndev/glass-fence:remmina` - for remote desktop connection (by @lowne).
  - Pass env var `REMMINA_URL=<proto>://[<username>[:<password>]@]server[:port]` (proto being `vnc`, `rdp` or `spice`).
  - Or create your custom configuration with remmina locally (it's saved in `~/.local/share/remmina/path_to_profile.remmina`) and bind-mount it, then pass env var `REMMINA_PROFILE=<path_to_profile.remmina>`.
- `arxndev/glass-fence:vlc` - for VLC Video player (needs volume mounted to `/media` with local video files, or setting `VLC_MEDIA=/media` path).
- `arxndev/glass-fence:xfce` or `arxndev/glass-fence:kde` - for a shared desktop / installing shared software.
- `arxndev/glass-fence:base` - for custom base.

Dockerhub images are built using GitHub actions on every push and on weekly basis to keep all browsers up-to-date.

All images are also available on [GitHub Container Registry](https://github.com/arxndev?tab=packages&repo_name=glass-fence) for faster pulls:

- `arxndevv/glass-fence/firefox:latest`
- `arxndevv/glass-fence/chromium:latest`
- `arxndevv/glass-fence/google-chrome:latest`
- `arxndevv/glass-fence/ungoogled-chromium:latest`
- `arxndevv/glass-fence/microsoft-edge:latest`
- `arxndevv/glass-fence/brave:latest`
- `arxndevv/glass-fence/vivaldi:latest`
- `arxndevv/glass-fence/opera:latest`
- `arxndevv/glass-fence/tor-browser:latest`
- `arxndevv/glass-fence/remmina:latest`
- `arxndevv/glass-fence/vlc:latest`
- `arxndevv/glass-fence/xfce:latest`
- `arxndevv/glass-fence/kde:latest`

For ARM-based images (like Raspberry Pi - with GPU hardware acceleration, Oracle Cloud ARM tier). Currently, not all images are available for ARM, because not all applications are available for ARM.

:::danger IMPORTANT
`arxndev/glass-fence:arm-*` images from dockerhub are currently not maintained and they can contain outdated software.
:::

Please use images below:

- `arxndevv/glass-fence/arm-firefox:latest`
- `arxndevv/glass-fence/arm-chromium:latest`
- `arxndevv/glass-fence/arm-ungoogled-chromium:latest`
- `arxndevv/glass-fence/arm-vlc:latest`
- `arxndevv/glass-fence/arm-xfce:latest`

For images with VAAPI GPU hardware acceleration using intel drivers use:

- `arxndevv/glass-fence/intel-firefox:latest`
- `arxndevv/glass-fence/intel-chromium:latest`
- `arxndevv/glass-fence/intel-google-chrome:latest`
- `arxndevv/glass-fence/intel-ungoogled-chromium:latest`
- `arxndevv/glass-fence/intel-microsoft-edge:latest`
- `arxndevv/glass-fence/intel-brave:latest`
- `arxndevv/glass-fence/intel-vivaldi:latest`
- `arxndevv/glass-fence/intel-opera:latest`
- `arxndevv/glass-fence/intel-tor-browser:latest`
- `arxndevv/glass-fence/intel-remmina:latest`
- `arxndevv/glass-fence/intel-vlc:latest`
- `arxndevv/glass-fence/intel-xfce:latest`
- `arxndevv/glass-fence/intel-kde:latest`

For images with Nvidia GPU hardware acceleration using EGL (see example below) use (please note, there is a known issue with EGL and Chromium-based browsers, see [here](https://github.com/ARXNDEV/glass-fence/issues/279)):

- `arxndevv/glass-fence/nvidia-firefox:latest`
- `arxndevv/glass-fence/nvidia-chromium:latest`
- `arxndevv/glass-fence/nvidia-google-chrome:latest`
- `arxndevv/glass-fence/nvidia-microsoft-edge:latest`
- `arxndevv/glass-fence/nvidia-brave:latest`

GHCR images are built using GitHub actions for every tag.

:::tip
For more applications, check out [arxndev/glass-fence-apps](https://github.com/ARXNDEV/glass-fence-apps).
:::

### Networking:
- If you want to use Glass Fence in **external** network, you can omit `GF_NAT1TO1`. It will automatically get your Public IP.
- If you want to use Glass Fence in **internal** network, set `GF_NAT1TO1` to your local IP address (e.g. `GF_NAT1TO1: 192.168.1.20`)-

Currently, it is not supported to supply multiple NAT addresses directly to glass-fence  (see https://github.com/ARXNDEV/glass-fence/issues/47).

But it can be acheived by deploying own turn server alongside glass-fence that is accessible from your LAN:

```yaml
version: "3.4"

services:
  glass-fence:
    image: "arxndev/glass-fence:firefox"
    restart: "unless-stopped"
    shm_size: "2gb"
    ports:
    - "8080:8080"
    - "52000-52100:52000-52100/udp"
    environment:
      GF_SCREEN: 1920x1080@30
      GF_PASSWORD: glass-fence
      GF_PASSWORD_ADMIN: admin
      GF_EPR: 52000-52100
      # highlight-start
      GF_ICESERVERS: |
        [{
          "urls": [ "turn:<MY-COTURN-SERVER>:3478" ],
          "username": "glass-fence",
          "credential": "glass-fence"
        },{
          "urls": [ "stun:stun.nextcloud.com:3478" ]
        }]
      # highlight-end
  coturn:
    image: 'coturn/coturn:latest'
    network_mode: "host"
    command: |
      -n
      --realm=localhost
      --fingerprint
      --listening-ip=0.0.0.0
      --external-ip=<MY-COTURN-SERVER>
      --listening-port=3478
      --min-port=49160
      --max-port=49200
      --log-file=stdout
      --user=glass-fence:glass-fence
      --lt-cred-mech
```

- Replace `<MY-COTURN-SERVER>` with your LAN IP address, and allow ports `49160-49200/udp` and `3478/tcp` in your LAN.
- Make sure you don't use `GF_ICELITE: true` because ICE LITE does not support TURN servers.

This setup adds local turn server to glass-fence. It won't be reachable by your remote clients and your own IP won't be reachable from your lan. So it effectively just adds local candidate and allows connections from LAN.

### Why so many ports?
- WebRTC needs UDP ports in order to transfer Audio/Video towards user and Mouse/Keyboard events to the server in real time.
- If you don't set `GF_ICELITE=true`, every user will need 2 UDP ports.
- If you set `GF_ICELITE=true`, every user will need only 1 UDP port. It is **recommended** to use *ice-lite*.
- Do not forget, they are **UDP** ports, that configuration must be correct in your firewall/router/docker.
- You can freely limit number of UDP ports. But you can't map them to different ports.
  - This **WON'T** work: `32000-32100:52000-52100/udp`
- You can change API port (8080).
  - This **WILL** work: `3000:8080`

### Using mux instead of epr

When using a mux, not so many ports are needed.

```yaml
version: "3.4"
services:
  glass-fence:
    image: "arxndev/glass-fence:firefox"
    restart: "unless-stopped"
    shm_size: "2gb"
    ports:
    - "8080:8080"
    # highlight-start
    - "8081:8081/tcp"
    - "8082:8082/udp"
    # highlight-end
    environment:
      GF_SCREEN: 1920x1080@30
      GF_PASSWORD: glass-fence
      GF_PASSWORD_ADMIN: admin
      # highlight-start
      GF_TCPMUX: 8081
      GF_UDPMUX: 8082
      # highlight-end
      GF_ICELITE: 1
```


- When using mux, `GF_EPR` is ignored.
- Mux accepts only one port, not a range.
- You only need to expose maximum two ports for WebRTC on your router/firewall and have many users connected.
- It can even be the same port number, so e.g. `GF_TCPMUX: 8081` and `GF_UDPMUX: 8081`.
- The same port must be exposed from docker container, you can't map them to different ports. So `8082:8082` is OK, but `"5454:8082` will not work.
- You can use them alone (either TCP or UDP) when needed.
  - UDP is generally better for latency. But some networks block UDP so it is good to have TCP available as fallback.
- Still, using `GF_ICELITE=true` is recommended.

### Using turn servers instead of port forwarding

- If you don't want to use port forwarding, you can use turn servers.
- But you need to have your own turn server (e.g. [cotrun](https://github.com/coturn/coturn)) or have access to one.
- They are generally not free, because they require a lot of bandwidth.
- Please make sure that you correctly escape your turn server credentials in the environment variable or use aphostrophes.

```yaml
GF_ICESERVERS: '[{"urls": ["turn:<MY-COTURN-SERVER>:443?transport=udp", "turn:<MY-COTURN-SERVER>:443?transport=tcp", "turns:<MY-COTURN-SERVER>:443?transport=udp", "turns:<MY-COTURN-SERVER>:443?transport=tcp"], "credential": "<MY-COTURN-CREDENTIAL"}, {"urls": ["stun:stun.nextcloud.com:443"]}]'
```

### Want to customize and install own add-ons, set custom bookmarks?
- You would need to modify the existing policy file and mount it to your container.
- For Firefox, copy [this](https://github.com/ARXNDEV/glass-fence/blob/master/.docker/firefox/policies.json) file, modify and mount it as: ` -v '${PWD}/policies.json:/usr/lib/firefox/distribution/policies.json'`
- For Chromium, copy [this](https://github.com/ARXNDEV/glass-fence/blob/master/.docker/chromium/policies.json) file, modify and mount it as: ` -v '${PWD}/policies.json:/etc/chromium/policies/managed/policies.json'`
- For others, see where existing `policies.json` is placed in their `Dockerfile`.

#### Allow file uploading & downloading
- From security perspective, browser is not enabled to access local file data.
- If you want to enable this, you need to modify following policies:
```json
  "DownloadRestrictions": 0,
  "AllowFileSelectionDialogs": true,
  "URLAllowlist": [
      "file:///home/glassfence/Downloads"
  ],
```

### Want to preserve browser data between restarts?
- You need to mount browser profile as volume.
- For Firefox, that is this `/home/glassfence/.mozilla/firefox/profile.default` folder, mount it as: ` -v '${PWD}/data:/home/glassfence/.mozilla/firefox/profile.default'`
- For Chromium, that is this `/home/glassfence/.config/chromium` folder, mount it as: ` -v '${PWD}/data:/home/glassfence/.config/chromium'`
- For other chromium based browsers, see in `supervisord.conf` folder that is specified in `--user-data-dir`.

#### Allow persistent data in policies
- From security perspective, browser is set up to forget all cookies and browsing history when its closed.
- If you want to enable this, you need to modify following policies:
```json
  "DefaultCookiesSetting": 1,
  "RestoreOnStartup": 1,
```

### Nvidia GPU acceleration

:::danger
There is a known issue with EGL and Chromium-based browsers, see [WebGL not working for Nvidia Google Chrome 112.x](https://github.com/ARXNDEV/glass-fence/issues/279).
That means currently only Firefox is supported for Nvidia GPU acceleration.
:::

You need to have [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit) installed, start the container with `--gpus all` flag and use images built for nvidia (see above).

```bash
docker run -d --gpus all \
  -p 8080:8080 \
  -p 56000-56100:56000-56100/udp \
  -e GF_SCREEN=1920x1080@30 \
  -e GF_PASSWORD=glass-fence \
  -e GF_PASSWORD_ADMIN=admin \
  -e GF_EPR=56000-56100 \
  -e GF_NAT1TO1=192.168.1.10 \
  -e GF_ICELITE=1 \
  -e GF_VIDEO_CODEC=h264 \
  -e GF_HWENC=nvenc \
  --shm-size=2gb \
  --name glass-fence \
  arxndevv/glass-fence/nvidia-google-chrome:latest
```

If you want to use docker-compose, you can use this example:

```yaml title="docker-compose.yaml"
version: "3.4"
services:
  glass-fence:
    image: "arxndevv/glass-fence/nvidia-google-chrome:latest"
    restart: "unless-stopped"
    shm_size: "2gb"
    ports:
    - "8080:8080"
    - "56000-56100:56000-56100/udp"
    environment:
      GF_SCREEN: '1920x1080@30'
      GF_PASSWORD: glass-fence
      GF_PASSWORD_ADMIN: admin
      GF_EPR: 56000-56100
      GF_NAT1TO1: 192.168.1.10
      GF_VIDEO_CODEC: h264
      GF_HWENC: nvenc
    deploy:
      resources:
        reservations:
          devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

- You can verify that GPU is available inside the container by running `docker exec -it glass-fence nvidia-smi` command.
- You can verify that GPU is used for encoding by searching for `nvh264enc` in `docker logs glass-fence` output.
- If you don'ŧ specify `GF_HWENC: nvenc` environment variable, CPU encoding will be used but GPU will still be available for browser rendering.

Broadcast pipeline is not hardware accelerated by default. You can use this pipeline created by [@evilalmus](https://github.com/ARXNDEV/glass-fence/issues/276#issuecomment-1498362533).

```yaml
GF_BROADCAST_PIPELINE: |
  flvmux name=mux 
    ! rtmpsink location={url} pulsesrc device={device} 
    ! audio/x-raw,channels=2 
    ! audioconvert 
    ! voaacenc 
    ! mux.
  ximagesrc display-name={display} show-pointer=false use-damage=false 
    ! video/x-raw,framerate=30/1 
    ! videoconvert 
    ! queue 
    ! video/x-raw,format=NV12 
    ! nvh264enc name=encoder preset=low-latency-hq gop-size=25 spatial-aq=true temporal-aq=true bitrate=2800 vbv-buffer-size=2800 rc-mode=6 
    ! h264parse config-interval=-1 
    ! video/x-h264,stream-format=byte-stream,profile=high 
    ! h264parse 
    ! mux.
```

### Want to use VPN for your Glass Fence browsing?
- Check this out: https://github.com/ARXNDEV/glass-fence-vpn

### Want to have multiple rooms on demand?
- Check this out: https://github.com/ARXNDEV/glass-fence-rooms

### Want to use different Apps than Browser?
- Check this out: https://github.com/ARXNDEV/glass-fence-apps

### Accounts:
- There are no accounts, display name (a.k.a. username) can be freely chosen. Only password needs to match. Depending on which password matches, the visitor gets its privilege:
  - Anyone, who enters with `GF_PASSWORD` will be **user**.
  - Anyone, who enters with `GF_PASSWORD_ADMIN` will be **admin**.
- Disabling passwords is not possible. However, you can use following query parameters to create auto-join links:
  - Adding `?pwd=<password>` will prefill password.
  - Adding `?usr=<display-name>` will prefill username.
  - Adding `?cast=1` will hide all control and show only video.
  - Adding `?embed=1` will hide most additional components and show only video.
  - Adding `?volume=<0-1>` will set volume to given value.
  - Adding `?lang=<language>` will set language to given value.
  - Adding `?show_side=1` will show the sidebar on startup.
  - Adding `?mute_chat=1` will mute the chat on startup.
  - e.g. `http(s)://<URL:Port>/?pwd=glass-fence&usr=guest&cast=1`

### Screen size
- Only admins can change screen size.
- You can set a default screen size, but this size **MUST** be one from the list, that your server supports.
- You will get this list in frontend, where you can choose from.

### Clipboard sharing
- Browsers have certain requirements to allow clipboard sharing.
  - Your instance must be HTTPS.
  - Firefox does not support clipboard sharing.
  - Use Chrome for the best experience.
- If your browser does not support clipboard sharing:
  - Clipboard icon in the bottom right corner will be displayed for host.
  - It opens text area that can share clipboard content bi-directionally.
  - Only plain-text is supported.
