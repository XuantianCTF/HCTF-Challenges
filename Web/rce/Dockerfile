FROM php:8.2-apache

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

COPY index.php /var/www/html/index.php
COPY flag.txt /flag.txt

RUN chmod 644 /var/www/html/index.php /flag.txt

RUN chown -R www-data:www-data /var/www/html

EXPOSE 80
