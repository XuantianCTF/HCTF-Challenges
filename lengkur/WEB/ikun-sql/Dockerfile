FROM php:7.4-apache

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y mariadb-server && \
    docker-php-ext-install mysqli && \
    docker-php-ext-enable mysqli

COPY src/ /var/www/html/

COPY mysql/01init.sql /tmp/01init.sql

COPY docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY Picture/ /var/www/html/Picture/

RUN chown -R www-data:www-data /var/www/html/

ENTRYPOINT ["docker-entrypoint.sh"]
