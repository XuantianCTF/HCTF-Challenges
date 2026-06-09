FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i 's|deb.debian.org|mirrors.ustc.edu.cn|g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    build-essential \
    libpcre3 libpcre3-dev \
    zlib1g-dev \
    php-fpm \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN cd /tmp \
    && wget -q http://nginx.org/download/nginx-1.4.2.tar.gz \
    && tar xzf nginx-1.4.2.tar.gz \
    && cd nginx-1.4.2 \
    && sed -i 's/cd.current_salt\[0\] = ~salt\[0\];/\/\* patched \*\//' src/os/unix/ngx_user.c \
    && sed -i 's/cd.current_salt\[1\] = salt\[1\];/\/\* patched \*\//' src/os/unix/ngx_user.c \
    && ./configure \
        --prefix=/usr/local/nginx \
        --with-http_stub_status_module \
        --with-cc-opt="-Wno-error" \
    && make -j$(nproc) \
    && make install \
    && rm -rf /tmp/nginx-1.4.2*

RUN mkdir -p /var/www/html/uploadfiles && \
    mkdir -p /usr/local/nginx/html

COPY nginx.conf /usr/local/nginx/conf/nginx.conf
COPY index.php /var/www/html/index.php
COPY www.conf /usr/local/etc/php-fpm.d/zz-docker.conf

RUN cp /var/www/html/index.php /usr/local/nginx/html/index.php

COPY flag /flag
RUN chmod 444 /flag

RUN chown -R www-data:www-data /var/www/html/uploadfiles

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
