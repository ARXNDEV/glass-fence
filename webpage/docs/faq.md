# Frequently Asked Questions

### How to enable debug mode? {#debug-mode}

To see verbose information from the glass-fence server, you can enable debug mode using [`log.level=debug`](/docs/v3/configuration#log.level) or set the environment variable `GF_DEBUG=1`.

If you have issue with encoding, you can view the GStreamer debug information by setting the environment variable `GST_DEBUG=3`. Learn more about it on the [Gstreamer documentation](https://gstreamer.freedesktop.org/documentation/tutorials/basic/debugging-tools.html?gi-language=c#the-debug-log).

If you want to debug [Pion WebRTC](https://github.com/pion/webrtc), you can set the environment variable `PION_LOG_DEBUG=all`, available options are writen in the [Pion WebRTC codebase](https://github.com/pion/logging/blob/2d5402f6579f2579cc51a5bd9c1fac127a781abb/logging_test.go#L190-L194).

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
      GF_DESKTOP_SCREEN: 1920x1080@30
      GF_MEMBER_MULTIUSER_USER_PASSWORD: glass-fence
      GF_MEMBER_MULTIUSER_ADMIN_PASSWORD: admin
      GF_WEBRTC_EPR: 52000-52100
      # highlight-start
      GF_DEBUG: 1
      # highlight-end
```

And then view the logs using `docker logs -f glass-fence`.

To see verbose information from the glass-fence client, you need to visit the developer console in your browser. You can do this by pressing `F12` and then navigating to the `Console` tab.

### How to enable support for Chinese/Japanese/Korean input method? {#input-method}

There exists an extension [Google Input Tools](https://chrome.google.com/webstore/detail/mclkkofklkfljcocdinagocijmpgbhab) for Chrome that allows you to use Chinese input method.

### How can I embed the Glass Fence into web page without login prompt coming up for viewers? {#embed}

You can use the following URL to embed the Glass Fence into a web page without login prompt coming up for viewers:

```
http://<your-glass-fence-server-ip>:8080/?usr=glass-fence&pwd=glass-fence
```

https://stackoverflow.com/questions/15276929/how-to-make-a-video-fullscreen-when-it-is-placed-inside-an-iframe

Your iframe needs an attribute: `allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"` or more modern `allow="fullscreen *"`. For the second you can remove the star if your iframe has the same origin or replace it with your iframe origin.

### Can I use glass-fence without docker? {#without-docker}

Yes, you can, but it is not recommended. Glass Fence is based on Debian and uses Xorg and Pulseaudio. Just follow the steps in the Dockerfile to install all dependencies.

However, it is recommend to start with existing system that has GUI with desktop manager, is based on Xorg and uses Pulseaudio (e.g. Ubuntu Desktop 24.04). For that matter you only need to install gstreamer dependencies, configure pulseaudio properly and run glass-fence binary (you don't need to build it from scratch, you can copy it from docker image).

### Why does the clipboard button does not show up? {#clipboard-button}

When you are using HTTPS connection and a compatible host browser (currently only Chromium-based browsers) which supports the Clipboard API, the clipboard button will not show up. Instead, you can use the native clipboard functionality of your host browser.

### Why am I unable to install extensions in the Glass Fence browser? {#extensions}

The browser in Glass Fence uses policies to restrict the installation of extensions. You can either add extensions to the policy file or disable the policy.

