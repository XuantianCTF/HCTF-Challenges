FROM php:7.4-apache


COPY src/ /var/www/html/

RUN touch /flag && chown www-data:www-data /flag && chmod 644 /flag

RUN chown -R www-data:www-data /var/www/html/ && chmod -R 755 /var/www/html


