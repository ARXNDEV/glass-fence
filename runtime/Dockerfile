ARG BASE_IMAGE=debian:trixie-slim
FROM $BASE_IMAGE AS runtime

#
# set custom user
ARG USERNAME=glassfence
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#
# install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        wget ca-certificates supervisor \
        pulseaudio dbus-x11 xserver-xorg-video-dummy \
        libcairo2 libxcb1 libxrandr2 libxv1 libopus0 libvpx9 libx264-164 libvo-aacenc0 librtmp1 libxcvt0 \
        #
        # needed for profile upload preStop hook
        zip curl \
        #
        # file chooser handler, clipboard, drop
        xdotool xclip libgtk-3-0 \
        #
        # gst
        gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
        gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
        gstreamer1.0-pulseaudio; \
    #
    # create a non-root user
    groupadd --gid $USER_GID $USERNAME; \
    useradd --uid $USER_UID --gid $USERNAME --shell /bin/bash --create-home $USERNAME; \
    adduser $USERNAME audio; \
    adduser $USERNAME video; \
    adduser $USERNAME pulse; \
    #
    # workaround for an X11 problem: http://blog.tigerteufel.de/?p=476
    mkdir /tmp/.X11-unix; \
    chmod 1777 /tmp/.X11-unix; \
    chown $USERNAME /tmp/.X11-unix/; \
    #
    # make directories for glass-fence
    mkdir -p /etc/glass-fence /var/www /var/log/glass-fence \
        /tmp/runtime-$USERNAME \
        /home/$USERNAME/.config/pulse  \
        /home/$USERNAME/.local/share/xorg; \
    chmod 1777 /var/log/glass-fence; \
    chmod 0700 /tmp/runtime-$USERNAME; \
    chown $USERNAME /var/log/glass-fence/ /tmp/runtime-$USERNAME; \
    chown -R $USERNAME:$USERNAME /home/$USERNAME; \
    #
    # install fonts
    apt-get install -y --no-install-recommends \
        # Emojis
        fonts-noto-color-emoji \
        # Chinese fonts
        fonts-arphic-ukai fonts-arphic-uming \
        fonts-wqy-zenhei xfonts-intl-chinese xfonts-wqy \
        # Japanese fonts
        fonts-ipafont-mincho fonts-ipafont-gothic \
        fonts-takao-mincho \
        # Korean fonts
        fonts-unfonts-core \
        fonts-wqy-microhei \
        # Indian fonts
        fonts-indic; \
    #
    # clean up
    apt-get clean -y; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

#
# copy runtime configs
COPY --chown=glassfence:glassfence .Xresources /home/$USERNAME/.Xresources
COPY dbus /usr/bin/dbus
COPY default.pa /etc/pulse/default.pa
COPY supervisord.conf /etc/glass-fence/supervisord.conf
COPY supervisord.dbus.conf /etc/glass-fence/supervisord.dbus.conf
COPY xorg.conf /etc/glass-fence/xorg.conf

#
# copy runtime folders
COPY --chown=glassfence:glassfence icon-theme /home/$USERNAME/.icons/default
COPY fontconfig/* /etc/fonts/conf.d/
COPY fonts /usr/local/share/fonts

#
# set default envs
ENV USER=$USERNAME
ENV DISPLAY=:99.0
ENV PULSE_SERVER=unix:/tmp/pulseaudio.socket
ENV XDG_RUNTIME_DIR=/tmp/runtime-$USERNAME
ENV GF_SERVER_BIND=:8080
ENV GF_PLUGINS_ENABLED=true
ENV GF_PLUGINS_DIR=/etc/glass-fence/plugins/

#
# add healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=8 \
    CMD wget -O - http://localhost:${GF_SERVER_BIND#*:}/health || \
        wget --no-check-certificate -O - https://localhost:${GF_SERVER_BIND#*:}/health || \
        exit 1

#
# run glass-fence
CMD ["/usr/bin/supervisord", "-c", "/etc/glass-fence/supervisord.conf"]
