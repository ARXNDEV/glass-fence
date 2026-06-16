ARG BASE_IMAGE=arxndevv/glass-fence-base:latest
FROM $BASE_IMAGE

# install remmina
RUN set -eux; apt-get update; \
    apt-get install -y --no-install-recommends \
      remmina-plugin-rdp remmina-plugin-vnc \
      remmina-plugin-x2go remmina-plugin-www; \
    # clean up
    apt-get clean -y; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# copy configuation files
COPY supervisord.conf /etc/glass-fence/supervisord/remmina.conf
COPY --chown=glassfence remmina.pref /home/glassfence/.config/remmina/remmina.pref
COPY --chown=glassfence rdp.remmina spice.remmina vnc.remmina /home/glassfence/.local/share/remmina/
COPY run-remmina.sh /usr/bin/run-remmina.sh
ENV REMMINA_URL=
ENV REMMINA_PROFILE=
