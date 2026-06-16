---
sidebar_position: 5
---

# Configuration

Config values can be set using three methods, sorted on this page by priority.

Example, setting `nat1to1` variable:
- As env variable: `GF_NAT1TO1=<ip>`
- As argument: `--nat1to1=<ip>`
- In YAML config file:
```yaml
nat1to1: <ip>
```

## Environment variables

#### `GF_SCREEN`:
  - Resolution after startup. Only Admins can change this later.
  - e.g. `1920x1080@30`
#### `GF_PASSWORD`:
  - Password for the user login.
  - e.g. `user_password`
#### `GF_PASSWORD_ADMIN`:
  - Password for the admin login.
  - e.g. `admin_password`
#### `GF_CONTROL_PROTECTION`:
  - Control protection means, users can gain control only if at least one admin is in the room.
  - e.g. `false`
#### `GF_IMPLICIT_CONTROL`:
  - If enabled members can gain control implicitly, they don't need to request control.
  - e.g. `false`
#### `GF_LOCKS`:
  - Resources, that will be locked when starting, separated by whitespace.
  - Currently supported:
    - `control`
    - `login`
    - `file_transfer`
  - e.g. `control`

### WebRTC

#### `GF_EPR`:
  - For WebRTC needed range of UDP ports.
  - e.g. `52000-52099`
#### `GF_UDPMUX`:
  - Alternative to epr with only one UDP port.
  - e.g. `52100`
#### `GF_TCPMUX`:
  - Use TCP connection, meant as fallback for UDP.
  - e.g. `52100`
#### `GF_NAT1TO1`:
  - IP of the server that will be sent to client, if not specified, public IP is automatically resolved.
  - e.g. `10.0.0.1`
#### `GF_IPFETCH`:
  - Automatically fetch IP address from given URL when `nat1to1` is not specified.
  - e.g. `http://checkip.amazonaws.com`
#### `GF_ICELITE`:
  - Use the ice lite protocol.
  - e.g. `false`
#### `GF_ICESERVER`:
  - Describes a single STUN and TURN server that can be used by the ICEAgent to establish a connection with a peer (simple usage for server without authentication).
  - e.g. `stun:stun.l.google.com:19302`
#### `GF_ICESERVERS`:
  - Describes multiple STUN and TURN server that can be used by the ICEAgent to establish a connection with a peer.
  - e.g. `[{"urls": ["turn:turn.example.com:19302", "stun:stun.example.com:19302"], "username": "name", "credential": "password"}, {"urls": ["stun:stun.example2.com:19302"]}]`
  - [More information](https://developer.mozilla.org/en-US/docs/Web/API/RTCIceServer)

### Video

#### `GF_VIDEO_CODEC`:
  - vp8 *(default encoder)*
  - vp9 *(parameter not optimized yet)*
  - h264 *(second best option)*
#### `GF_VIDEO_BITRATE`:
  - Bitrate of the video stream in kb/s.
  - e.g. 3500
#### `GF_VIDEO`:
  - Makes it possible to create custom gstreamer video pipeline. With this you could find the best quality for your CPU.
  - Installed are
    - `gstreamer1.0-plugins-base`
    - `gstreamer1.0-plugins-good`
    - `gstreamer1.0-plugins-bad`
    - `gstreamer1.0-plugins-ugly`
  - e.g. `ximagesrc display-name=%s show-pointer=true use-damage=false ! video/x-raw,framerate=30/1 ! videoconvert ! queue ! video/x-raw,format=NV12 ! x264enc threads=4 bitrate=3500 key-int-max=60 vbv-buf-capacity=4000 byte-stream=true tune=zerolatency speed-preset=veryfast ! video/x-h264,stream-format=byte-stream,profile=constrained-baseline`
#### `GF_MAX_FPS`:
  - The resulting stream frames per seconds should be capped *(0 for uncapped)*.
  - e.g. `0`
#### `GF_HWENC`:
  - none *(default CPU encoding)*
  - vaapi
  - nvenc

### Audio

#### `GF_AUDIO_CODEC`:
  - opus *(default encoder)*
  - g722
  - pcmu
  - pcma
#### `GF_AUDIO_BITRATE`:
  - Bitrate of the audio stream in kb/s.
  - e.g. `196`
#### `GF_AUDIO`:
  - Makes it possible to create custom gstreamer audio pipeline, same as for video.
  e.g. `pulsesrc device=%s ! audio/x-raw,channels=2 ! audioconvert ! opusenc bitrate=128000`

### Broadcast

#### `GF_BROADCAST_PIPELINE`:
  - Makes it possible to create custom gstreamer pipeline used for broadcasting, strings `{url}`, `{device}` and `{display}` will be replaced.
#### `GF_BROADCAST_URL`:
  - Set a default URL for broadcast streams. It can be disabled/changed later by admins in the GUI.
  - e.g. `rtmp://<your-server>:1935/ingest/<stream-key>`
#### `GF_BROADCAST_AUTOSTART`:
  - Automatically start broadcasting when glass-fence starts and broadcast_url is set.
  - e.g. `true`
### Server

#### `GF_BIND`:
  - Address/port/socket where glass-fence binds to *(default 127.0.0.1:8080)*.
  - e.g. `:8080`
#### `GF_CERT`:
  - Path to the SSL-Certificate.
  - e.g. `/certs/cert.pem`
#### `GF_KEY`:
  - Path to the SSL-Certificate private key.
  - e.g. `/certs/key.pem`
#### `GF_PROXY`:
  - Enable reverse proxy mode, so that glass-fence trusts `X-Forwarded-For` headers.
  - e.g. `false`
#### `GF_PATH_PREFIX`:
  - Path prefix for HTTP requests.
  - e.g. `/glass-fence/`
#### `GF_CORS`:
  - Cross origin request sharing, whitespace separated list of allowed hosts, `*` for all.
  - e.g. `127.0.0.1 glass-fence.example.com`

### File Transfer

#### `GF_FILE_TRANSFER_ENABLED`:
  - Enable file transfer feature.
  - e.g. `true`
#### `GF_FILE_TRANSFER_PATH`:
  - Path where files will be transferred between the host and users. By default, this is
  `/home/glassfence/Downloads`. If the path doesn't exist, it will be created.
  - e.g. `/home/glassfence/Desktop`

### Expert settings

#### `GF_DISPLAY`:
  - XDisplay to capture.
#### `GF_DEVICE`:
  - Audio device be to captured.
#### `GF_STATIC`:
  - Path to glass-fence client files to serve.

## Arguments

You can execute `glass-fence serve --help` to see available arguments.

```
Usage:
  glass-fence serve [flags]

Flags:
      --audio string                audio codec parameters to use for streaming
      --audio_bitrate int           audio bitrate in kbit/s (default 128)
      --audio_codec string          audio codec to be used (default "opus")
      --bind string                 address/port/socket to serve glass-fence (default "127.0.0.1:8080")
      --broadcast_pipeline string   custom gst pipeline used for broadcasting, strings {url} {device} {display} will be replaced
      --broadcast_url string        URL for broadcasting, setting this value will automatically enable broadcasting
      --cert string                 path to the SSL cert used to secure the glass-fence server
      --control_protection          control protection means, users can gain control only if at least one admin is in the room
      --cors strings                list of allowed origins for CORS (default [*])
      --device string               audio device to capture (default "audio_output.monitor")
      --display string              XDisplay to capture (default ":99.0")
      --epr string                  limits the pool of ephemeral ports that ICE UDP connections can allocate from (default "59000-59100")
      --file_transfer_enabled       enable file transfer feature (default false)
      --file_transfer_path string   path to use for file transfer (default "/home/glassfence/Downloads")
      --g722                        DEPRECATED: use audio_codec
      --h264                        DEPRECATED: use video_codec
  -h, --help                        help for serve
      --hwenc string                use hardware accelerated encoding
      --icelite                     configures whether or not the ice agent should be a lite agent
      --iceserver strings           describes a single STUN and TURN server that can be used by the ICEAgent to establish a connection with a peer (default [stun:stun.l.google.com:19302])
      --iceservers string           describes a single STUN and TURN server that can be used by the ICEAgent to establish a connection with a peer
      --implicit_control            if enabled members can gain control implicitly
      --ipfetch string              automatically fetch IP address from given URL when nat1to1 is not present (default "http://checkip.amazonaws.com")
      --key string                  path to the SSL key used to secure the glass-fence server
      --locks strings               resources, that will be locked when starting (control, login)
      --max_fps int                 maximum fps delivered via WebRTC, 0 is for no maximum (default 25)
      --nat1to1 strings             sets a list of external IP addresses of 1:1 (D)NAT and a candidate type for which the external IP address is used
      --opus                        DEPRECATED: use audio_codec
      --password string             password for connecting to stream (default "glass-fence")
      --password_admin string       admin password for connecting to stream (default "admin")
      --path_prefix string          path prefix for HTTP requests (default "/")
      --pcma                        DEPRECATED: use audio_codec
      --pcmu                        DEPRECATED: use audio_codec
      --proxy                       enable reverse proxy mode
      --screen string               default screen resolution and framerate (default "1280x720@30")
      --static string               path to glass-fence client files to serve (default "./www")
      --tcpmux int                  single TCP mux port for all peers
      --udpmux int                  single UDP mux port for all peers
      --video string                video codec parameters to use for streaming
      --video_bitrate int           video bitrate in kbit/s (default 3072)
      --video_codec string          video codec to be used (default "vp8")
      --vp8                         DEPRECATED: use video_codec
      --vp9                         DEPRECATED: use video_codec

Global Flags:
      --config string   configuration file path
  -d, --debug           enable debug mode
  -l, --logs            save logs to file
```

## Config file

You can mount YAML config file to docker container on this path `/etc/glass-fence/glass-fence.yaml` and store your configuration there.

Config uses the keys from arguments, that can be viewed in program's help output.

Example (with just some of the available arguments):

```yaml
# audio bitrate in kbit/s
audio_bitrate: 128

# video bitrate in kbit/s
video_bitrate: 3072

# maximum fps delivered via WebRTC, 0 is for no maximum
max_fps: 25

# password for connecting to stream
password: "glass-fence"

# admin password for connecting to stream
password_admin: "admin"

# default screen resolution and framerate
screen: "1280x720@30"

# limits the pool of ephemeral ports that ICE UDP connections can allocate from
epr: "59000-59100"
```
