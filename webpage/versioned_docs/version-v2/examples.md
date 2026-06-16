---
sidebar_position: 3
---

# Examples

## Firefox

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
    volumes:
      - <your-host-path>:/home/glassfence/.mozilla/firefox # persist firexfox settings
    environment:
      GF_SCREEN: '1920x1080@30'
      GF_PASSWORD: glass-fence
      GF_PASSWORD_ADMIN: admin
      GF_EPR: 52000-52100
      GF_NAT1TO1: <your-IP>
```

## Chromium

```yaml
version: "3.4"
services:
  glass-fence:
    image: "arxndev/glass-fence:chromium"
    restart: "unless-stopped"
    shm_size: "2gb"
    ports:
      - "8080:8080"
      - "52000-52100:52000-52100/udp"
    environment:
      GF_SCREEN: '1920x1080@30'
      GF_PASSWORD: glass-fence
      GF_PASSWORD_ADMIN: admin
      GF_EPR: 52000-52100
      GF_NAT1TO1: <your-IP>
```

## VLC

```yaml
version: "3.4"
services:
  glass-fence:
    image: "arxndev/glass-fence:vlc"
    restart: "unless-stopped"
    shm_size: "2gb"
    volumes:
      - "<your-video-folder>:/video" 
    ports:
      - "8080:8080"
      - "52000-52100:52000-52100/udp"
    environment:
      GF_SCREEN: '1920x1080@30'
      GF_PASSWORD: glass-fence
      GF_PASSWORD_ADMIN: admin
      GF_EPR: 52000-52100
      GF_NAT1TO1: <your-IP>
```

## Raspberry Pi

```yaml
version: "3.4"
services:
  glass-fence:
    # see docs for more variants
    image: "arxndevv/glass-fence/arm-chromium:latest"
    restart: "unless-stopped"
    # increase on rpi's with more then 1gb ram.
    shm_size: "520mb"
    ports:
      - "8088:8080"
      - "52000-52100:52000-52100/udp"
    # note: this is important since we need a GPU for hardware acceleration alternatively
    #       mount the devices into the docker.
    privileged: true
    environment:
      GF_SCREEN: '1280x720@30'
      GF_PASSWORD: 'glass-fence'
      GF_PASSWORD_ADMIN: 'admin'
      GF_EPR: 52000-52100
      # note: when setting GF_VIDEO, then variables GF_MAX_FPS and GF_VIDEO_BITRATE
      #       are not being used, you can adjust them in this variable.
      GF_VIDEO: |
        ximagesrc display-name=%s use-damage=0 show-pointer=true use-damage=false
          ! video/x-raw,framerate=30/1
          ! videoconvert
          ! queue
          ! video/x-raw,framerate=30/1,format=NV12
          ! v4l2h264enc extra-controls="controls,h264_profile=1,video_bitrate=1250000;"
          ! h264parse config-interval=3
          ! video/x-h264,stream-format=byte-stream,profile=constrained-baseline
      GF_VIDEO_CODEC: h264
```

## Not using docker?

You can execute `glass-fence --help` to see available arguments. In [Dockerfile](https://github.com/ARXNDEV/glass-fence/blob/master/.docker/base/Dockerfile) you can find required dependencies and install them manually.
