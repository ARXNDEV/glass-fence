ARG BASE_IMAGE=arxndevv/glass-fence-base:latest
FROM $BASE_IMAGE

#
# install waterfox
RUN set -eux; apt-get update; \
    apt-get install -y --no-install-recommends openbox \
    xz-utils bzip2 libgtk-3-0 libdbus-glib-1-2; \
    #
    # fetch latest release
    LATEST=$(curl -s https://api.github.com/repos/BrowserWorks/Waterfox/releases/latest | grep -oP '"tag_name": "\K[^"]+'); \
    wget -O /tmp/waterfox-setup.tar.bz2 "https://cdn.waterfox.com/waterfox/releases/${LATEST}/Linux_x86_64/waterfox-${LATEST}.tar.bz2"; \
    mkdir /usr/lib/waterfox; \
    tar -xjf /tmp/waterfox-setup.tar.bz2 -C /usr/lib; \
    rm -f /tmp/waterfox-setup.tar.bz2; \
    ln -s /usr/lib/waterfox/waterfox /usr/bin/waterfox; \
    #
    # create a profile directory
    mkdir -p /home/glassfence/.waterfox/profile.default/extensions; \
    chown -R glass-fence:glass-fence /home/glassfence/.waterfox/profile.default; \
    #
    # clean up
    apt-get --purge autoremove -y xz-utils bzip2; \
    apt-get clean -y; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

#
# copy configuation files
COPY supervisord.conf /etc/glass-fence/supervisord/waterfox.conf
COPY glass-fence.js /usr/lib/waterfox/mozilla.cfg
COPY autoconfig.js /usr/lib/waterfox/defaults/pref/autoconfig.js
COPY policies.json /usr/lib/waterfox/distribution/policies.json
COPY --chown=glass-fence profiles.ini /home/glassfence/.waterfox/profiles.ini
COPY openbox.xml /etc/glass-fence/openbox.xml
