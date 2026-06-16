---
sidebar_position: 7
---

# Frequently Asked Questions

## How to enable debug mode?

To see verbose information from Glass Fence server, you can enable debug mode using `GF_DEBUG`.

```yaml title="docker-compose.yaml"
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
      GF_DEBUG: 1
      # highlight-end
```

Ensure, that you have enabled debug mode in javascript console too, in order to see verbose information from client.

## Chinese input method is not working

There exists an extension [Google Input Tools](https://chrome.google.com/webstore/detail/mclkkofklkfljcocdinagocijmpgbhab) for Chrome that allows you to use Chinese input method.

## How can I embed the Glass Fence desktop into web page without login prompt coming up for viewers?

You can use the following URL to embed the Glass Fence desktop into a web page without login prompt coming up for viewers:

```
http://<your-glass-fence-server-ip>:8080/?usr=glass-fence&pwd=glass-fence
```

https://stackoverflow.com/questions/15276929/how-to-make-a-video-fullscreen-when-it-is-placed-inside-an-iframe

Your iframe needs an attribute: `allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"` or more modern `allow="fullscreen *"`. For the second you can remove the star if your iframe has the same origin or replace it with your iframe origin.

## Can I use glass-fence without docker?

It is strongly recommended to use Glass Fence with Docker, as it is the easiest way to run it. But you should be able to install Glass Fence "natively" on your host system. Glass Fence is based on Debian and uses Xorg and Pulseaudio. You would just need to follow steps that are in Dockerfile, install all dependencies on your host system and then just run it.

However, it is recommend to start with existing system that has GUI with desktop manager, is based on Xorg and uses Pulseaudio (e.g. Ubuntu Desktop 22.04). For that matter you only need to install gstreamer dependencies, configure pulseaudio properly and run glass-fence binary (you don't need to build it from scratch, you can copy it from docker image).
