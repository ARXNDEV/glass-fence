ARG BASE_IMAGE=arxndevv/glass-fence-base:latest
FROM $BASE_IMAGE

#
# install kde
RUN set -eux; apt-get update; \
    apt-get install -y --no-install-recommends kde-full kwin-x11 libkf5config-bin sudo; \
    #
    # add user to sudoers
    usermod -aG sudo glass-fence; \
    echo "glass-fence:glass-fence" | chpasswd; \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers; \
    # clean up
    apt remove xserver-xorg-legacy -y; \
    apt-get clean -y; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

#
# disable autolock
RUN kwriteconfig5 --file /home/glassfence/.config/kscreenlockerrc --group Daemon --key Autolock false; \
    chown glass-fence:glass-fence /home/glassfence/.config/kscreenlockerrc

#
# copy configuation files
COPY supervisord.conf /etc/glass-fence/supervisord/kde.conf

