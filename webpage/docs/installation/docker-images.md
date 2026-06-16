---
description: List of available Neko Docker images and their flavors.
---

import { AppIcon } from '@site/src/components/AppIcon';

# Docker Images

Neko as a standalone streaming server is available as a Docker image. But that is rarely interesting for general use. The real power of Neko is in its ability to accommodate custom applications in the virtual desktop environment. This is where the various flavors of Neko Docker images come in.

The base image is available as multi-arch image at [`arxndevv/glass-fence/base`](https://arxndevv/glass-fence/base). See [Supported Architectures](#arch) for more information.

## Naming Convention {#naming}

Neko images are available on two public registries. The [GitHub Container Registry (GHCR)](#ghcr.io) hosts stable releases with all flavors and architectures. The latest development version of the Neko image for the AMD64 architecture is available on [Docker Hub](#docker.io).

:::info
You should always prefer the GHCR registry, as it supports flavors and specific versions, unless you want to test the latest development version.
:::

### GitHub Container Registry (GHCR) {#ghcr.io}

Neko Docker images are available on the [GitHub Container Registry (GHCR)](https://github.com/m1k1o?tab=packages&repo_name=neko). The naming convention for Neko Docker images is as follows:

```
arxndevv/glass-fence/[<flavor>-]<application>:<version>
```

- `<flavor>` is the optional flavor of the image. See [Available Flavors](#flavors) for more information.
- `<application>` is the application name or base image. See [Available Applications](#apps) for more information.
- `<version>` is the version of the image. See [Versioning](#ghcr.io-versioning) for more information.

#### Versioning scheme {#ghcr.io-versioning}

The versioning scheme follows the [Semantic Versioning 2.0.0](https://semver.org/) specification. The following tags are available for each image:

- `latest` - Points to the most recent stable release.
- `MAJOR` - Tracks the latest release within the specified major version.
- `MAJOR.MINOR` - Tracks the latest release within the specified major and minor version.
- `MAJOR.MINOR.PATCH` - Refers to a specific release.

For example:
- `arxndevv/glass-fence/firefox:latest` - Latest stable version.
- `arxndevv/glass-fence/firefox:3` - Latest release in the 3.x.x series.
- `arxndevv/glass-fence/firefox:3.0` - Latest release in the 3.0.x series.
- `arxndevv/glass-fence/firefox:3.0.0` - Specific version 3.0.0.

A full list of published versions can be found in the [GitHub tags](https://github.com/ARXNDEV/glass-fence/tags).

### Docker Hub {#docker.io}

An alternative registry is available on [Docker Hub](https://hub.docker.com/r/m1k1o/neko). This registry hosts images built from the latest code in the [master branch](https://github.com/ARXNDEV/glass-fence/tree/master). However, it only includes images without flavors and supports the AMD64 architecture. The naming convention for these images is as follows:

```
m1k1o/neko:<application>
```

- `<application>` is the application name or base image. See [Available Applications](#apps) for more information.

:::info
`m1k1o/neko:latest` is an alias for `m1k1o/neko:firefox` due to historical reasons. It is recommended to use the `arxndevv/glass-fence/firefox:latest` image instead.
:::

## Available Applications {#apps}

The following applications are available as Neko Docker images:

### Firefox-based browsers {#firefox-based-browsers}

In comparison to Chromium-based browsers, Firefox-based browsers do not require additional capabilities or a bigger shared memory size to not crash.

| Icon | Name | Docker Image |
| ---- | ---- | ------------ |
| <AppIcon id="firefox" /> | [Firefox](https://www.mozilla.org/firefox/) <br /> The open-source browser from Mozilla. | [`arxndevv/glass-fence/firefox`](https://arxndevv/glass-fence/firefox) |
| <AppIcon id="tor-browser" /> | [Tor Browser](https://www.torproject.org/) <br /> A browser designed to access the Tor network for enhanced privacy. | [`arxndevv/glass-fence/tor-browser`](https://arxndevv/glass-fence/tor-browser) |
| <AppIcon id="waterfox" /> | [Waterfox](https://www.waterfox.net/) <br /> A privacy-focused browser based on Firefox. | [`arxndevv/glass-fence/waterfox`](https://arxndevv/glass-fence/waterfox) |

:::warning
**Waterfox** is currently not built automatically, because Cloudflare blocks the download and therefore github actions are failing. You can build it manually to get the latest version.
:::

Check the [Firefox-based browsers customization guide](/docs/v3/customization/browsers#firefox-based) for more information on how to customize Firefox-based browsers (configuring profile, installing extensions, etc.).

### Chromium-based browsers {#chromium-based-browsers}

There are multiple flavors of Chromium-based browsers available as Neko Docker images.

Chromium is running with `--no-sandbox` flag, which is required to run it in a container without additional configuration. You can read more about it in [Quick introduction](https://www.google.com/googlebooks/chrome/med_26.html) to Chrome's sandbox. More in-depth [design document](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/design/sandbox.md), with internal links to FAQ, etc.

Additionally, chromium-based browsers require `--shm-size=2g` (or more) to work properly. This is because the default shared memory size for Docker containers is too small for Chromium-based browsers, which can lead to crashes and other issues. 

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="docker-run" label="Docker run command">

    ```bash
    docker run \
      --shm-size=2g \
      arxndevv/glass-fence/chromium
    ```

  </TabItem>

  <TabItem value="docker-compose" label="Docker Compose configuration">

    ```yaml title="docker-compose.yaml"
    shm_size: 2g
    ```

  </TabItem>
</Tabs>

| Icon | Name | Docker Image |
| ---- | ---- | ------------ |
| <AppIcon id="chromium" /> | [Chromium](https://www.chromium.org/chromium-projects/) <br /> The open-source project behind Google Chrome. | [`arxndevv/glass-fence/chromium`](https://arxndevv/glass-fence/chromium) |
| <AppIcon id="google-chrome" /> | [Google Chrome](https://www.google.com/chrome/) <br /> The most popular browser in the world. | [`arxndevv/glass-fence/google-chrome`](https://arxndevv/glass-fence/google-chrome) |
| <AppIcon id="ungoogled-chromium" /> | [Ungoogled Chromium](https://ungoogled-software.github.io/) <br /> A fork of Chromium without Google integration. | [`arxndevv/glass-fence/ungoogled-chromium`](https://arxndevv/glass-fence/ungoogled-chromium) |
| <AppIcon id="microsoft-edge" /> | [Microsoft Edge](https://www.microsoft.com/edge) <br/> The new Microsoft Edge is based on Chromium. | [`arxndevv/glass-fence/microsoft-edge`](https://arxndevv/glass-fence/microsoft-edge) |
| <AppIcon id="brave" /> | [Brave](https://brave.com/) <br /> A privacy-focused browser. | [`arxndevv/glass-fence/brave`](https://arxndevv/glass-fence/brave) |
| <AppIcon id="vivaldi" /> | [Vivaldi](https://vivaldi.com/) <br /> A highly customizable browser. | [`arxndevv/glass-fence/vivaldi`](https://arxndevv/glass-fence/vivaldi) |
| <AppIcon id="opera" /> | [Opera](https://www.opera.com/)* <br /> A fast and secure browser. | [`arxndevv/glass-fence/opera`](https://arxndevv/glass-fence/opera) |

\* requires extra steps to enable DRM, see instructions [here](https://www.reddit.com/r/operabrowser/wiki/opera/linux_widevine_config/). `libffmpeg` is already configured.

Check the [Chromium-based browsers customization guide](/docs/v3/customization/browsers#chromium-based) for more information on how to customize Chromium-based browsers (configuring profile, installing extensions, etc.).

### Desktop Environments {#desktop}

These images feature a full desktop environment where you can install and run multiple applications, use window management, and more. This is useful for people who want to run multiple applications in a single container.

| Icon | Name | Docker Image |
| ---- | ---- | ------------ |
| <AppIcon id="xfce" /> | [Xfce](https://xfce.org/) <br /> A lightweight desktop environment. | [`arxndevv/glass-fence/xfce`](https://arxndevv/glass-fence/xfce) |
| <AppIcon id="kde" /> | [KDE Plasma](https://kde.org/plasma-desktop) <br /> A feature-rich desktop environment. | [`arxndevv/glass-fence/kde`](https://arxndevv/glass-fence/kde) |

### Other Applications {#other}

As it would be impossible to include all possible applications in the repository, a couple of the most popular ones that work well with Neko have been chosen. Custom images can be created by using the base image and installing the desired application.

| Icon | Name | Docker Image |
| ---- | ---- | ------------ |
| <AppIcon id="remmina" /> | [Remmina](https://remmina.org/) <br /> A remote desktop client. | [`arxndevv/glass-fence/remmina`](https://arxndevv/glass-fence/remmina) |
| <AppIcon id="vlc" /> | [VLC](https://www.videolan.org/vlc/) <br /> A media player. | [`arxndevv/glass-fence/vlc`](https://arxndevv/glass-fence/vlc) |

#### Remmina Configuration {#remmina}

To use Remmina with Neko, you can either pass the `REMMINA_URL=<proto>://[<username>[:<password>]@]server[:port]` environment variable (proto being `vnc`, `rdp` or `spice`):

```bash
docker run \
  -e REMMINA_URL=vnc://server:5900 \
  arxndevv/glass-fence/remmina
```

Or bind-mount a custom configuration file to `~/.local/share/remmina/path_to_profile.remmina`. Then pass the `REMMINA_PROFILE=<path_to_profile.remmina>` environment variable:

```ini title="default.remmina"
[remmina]
name=Default
protocol=VNC
server=server.local
port=5900
```

```bash
docker run \
  -v /path/to/default.remmina:/root/.local/share/remmina/default.remmina \
  -e REMMINA_PROFILE=/root/.local/share/remmina/default.remmina \
  arxndevv/glass-fence/remmina
```

#### VLC Configuration {#vlc}

To use VLC with Neko, you can either pass the `VLC_MEDIA=<url>` environment variable:

```bash
docker run \
  -e VLC_MEDIA=http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4 \
  arxndevv/glass-fence/vlc
```

You can also bind-mount your local media files to the container, create a custom playlist, and pass the `VLC_MEDIA=<path_to_playlist>` environment variable:

```bash
docker run \
  -v /path/to/media:/media \
  -e VLC_MEDIA=/media/playlist.xspf \
  arxndevv/glass-fence/vlc
```

:::tip
See [neko-apps](https://github.com/ARXNDEV/glass-fence-apps) repository for more applications.
:::

## Available Flavors {#flavors}

:::danger Keep in Mind
Currently the focus is on CPU images (wihout any flavor). So the GPU support might not work as expected.
:::

The following flavors are available for Neko Docker images:

- `nvidia` - NVIDIA GPU support.
- `intel` - Intel GPU support.

### Intel (VAAPI GPU hardware acceleration) {#intel}

Only for architecture `linux/amd64`.

For images with VAAPI GPU hardware acceleration using Intel drivers use:

- [`arxndevv/glass-fence/intel-firefox`](https://arxndevv/glass-fence/intel-firefox)
- [`arxndevv/glass-fence/intel-waterfox`](https://arxndevv/glass-fence/intel-waterfox)
- [`arxndevv/glass-fence/intel-chromium`](https://arxndevv/glass-fence/intel-chromium)
- [`arxndevv/glass-fence/intel-google-chrome`](https://arxndevv/glass-fence/intel-google-chrome)
- [`arxndevv/glass-fence/intel-ungoogled-chromium`](https://arxndevv/glass-fence/intel-ungoogled-chromium)
- [`arxndevv/glass-fence/intel-microsoft-edge`](https://arxndevv/glass-fence/intel-microsoft-edge)
- [`arxndevv/glass-fence/intel-brave`](https://arxndevv/glass-fence/intel-brave)
- [`arxndevv/glass-fence/intel-vivaldi`](https://arxndevv/glass-fence/intel-vivaldi)
- [`arxndevv/glass-fence/intel-opera`](https://arxndevv/glass-fence/intel-opera)
- [`arxndevv/glass-fence/intel-tor-browser`](https://arxndevv/glass-fence/intel-tor-browser)
- [`arxndevv/glass-fence/intel-remmina`](https://arxndevv/glass-fence/intel-remmina)
- [`arxndevv/glass-fence/intel-vlc`](https://arxndevv/glass-fence/intel-vlc)
- [`arxndevv/glass-fence/intel-xfce`](https://arxndevv/glass-fence/intel-xfce)
- [`arxndevv/glass-fence/intel-kde`](https://arxndevv/glass-fence/intel-kde)

The base image is available at [`arxndevv/glass-fence/intel-base`](https://arxndevv/glass-fence/intel-base).

### Nvidia (CUDA GPU hardware acceleration) {#nvidia}

Only for architecture `linux/amd64`.

For images with Nvidia GPU hardware acceleration using EGL use:

- [`arxndevv/glass-fence/nvidia-firefox`](https://arxndevv/glass-fence/nvidia-firefox)
- [`arxndevv/glass-fence/nvidia-chromium`](https://arxndevv/glass-fence/nvidia-chromium)
- [`arxndevv/glass-fence/nvidia-google-chrome`](https://arxndevv/glass-fence/nvidia-google-chrome)
- [`arxndevv/glass-fence/nvidia-microsoft-edge`](https://arxndevv/glass-fence/nvidia-microsoft-edge)
- [`arxndevv/glass-fence/nvidia-brave`](https://arxndevv/glass-fence/nvidia-brave)

The base image is available at [`arxndevv/glass-fence/nvidia-base`](https://arxndevv/glass-fence/nvidia-base). See [Examples](/docs/v3/installation/examples#nvidia) for more information and usage.

## Supported Architectures {#arch}

Neko Docker images are built with docker buildx and are available for multiple architectures. The following architectures are supported by the base image:

- `linux/amd64` - 64-bit Intel/AMD architecture (most common).
- `linux/arm64` - 64-bit ARM architecture (e.g., Raspberry Pi 4, Apple M1/M2).

### Availability Matrix {#availability}

The availability of applications for ARM architecture is limited due to the lack of support for some applications. The following table shows the availability of each application for each architecture. The `✅` symbol indicates that the application is available for that architecture, while the `❌` symbol indicates that it is not available.

| Application                               | AMD64 | ARM64 | Reference |
| ----------------------------------------- | ----- | ----- | --------- |
| [Firefox](#firefox)                       | ✅    | ✅ \* | - |
| [Tor Browser](#tor-browser)               | ✅    | ❌    | [Forum Post](https://forum.torproject.org/t/tor-browser-for-arm-linux/5240) |
| [Waterfox](#waterfox)                     | ✅    | ❌    | [Github Issue](https://github.com/BrowserWorks/Waterfox/issues/1506), [Reddit](https://www.reddit.com/r/waterfox/comments/jpqsds/are_there_any_builds_for_arm64/) |
| [Chromium](#chromium)                     | ✅    | ✅ \* | - |
| [Google Chrome](#google-chrome)           | ✅    | ❌    | [Community Post](https://askubuntu.com/a/1383791) |
| [Ungoogled Chromium](#ungoogled-chromium) | ✅    | ❌    | [Downloads Page](https://ungoogled-software.github.io/ungoogled-chromium-binaries/) |
| [Microsoft Edge](#microsoft-edge)         | ✅    | ❌    | [Community Post](https://techcommunity.microsoft.com/discussions/edgeinsiderdiscussions/edge-for-linuxarm64/1532272) |
| [Brave](#brave)                           | ✅    | ✅ \* | - |
| [Vivaldi](#vivaldi)                       | ✅    | ✅ \* | - |
| [Opera](#opera)                           | ✅    | ❌    | [Forum Post](https://forums.opera.com/topic/52811/opera-do-not-support-arm64-on-linux) |
| [Xfce](#xfce)                             | ✅    | ✅    | - |
| [KDE](#kde)                               | ✅    | ✅    | - |
| [Remmina](#remmina)                       | ✅    | ✅    | - |
| [VLC](#vlc)                               | ✅    | ✅    | - |

\* No DRM support.

:::tip
[Oracle Cloud ARM free tier](https://www.oracle.com/cloud/free/) is a great way to test Neko on ARM architecture for free. You can use the `arxndevv/glass-fence/xfce` image to run a full desktop environment with Xfce and test the applications.
:::
