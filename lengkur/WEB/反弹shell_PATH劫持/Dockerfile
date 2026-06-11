FROM php:7.3-apache

WORKDIR /var/www/html

# 安装常用反弹工具
RUN apt-get update && apt-get install -y \
    socat \
    netcat-traditional \
    procps \
    iproute2 \
    python \
    && rm -rf /var/lib/apt/lists/*

COPY src/ /var/www/html/

COPY Cat /

COPY Cat.c /

RUN chown root:root /Cat && chmod 4755 /Cat

RUN echo "flag{testflag}" > /root/flag && chmod 400 /root/flag
RUN echo "I am flag" > /flag

CMD ["apache2-foreground"]
