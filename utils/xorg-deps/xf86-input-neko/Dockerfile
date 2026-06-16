FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
    apt-get update; \
    apt-get install -y \
        gcc pkgconf autoconf automake libtool make xorg-dev xutils-dev \
    && rm -rf /var/lib/apt/lists/*;

WORKDIR /app

COPY ./ /app/

RUN set -eux; \
    ./autogen.sh --prefix=/usr; \
    ./configure; \
    make -j$(nproc); \
    make install;

# docker build -t xf86-input-glass-fence .
# docker run -v $PWD/build:/app/build --rm xf86-input-glass-fence make install DESTDIR=/app/build
