#!/bin/bash

# Find php-fpm binary and config
PHP_FPM=$(which php-fpm7.4 || which php-fpm8.0 || which php-fpm7.3 || find /usr/sbin /usr/bin -name 'php-fpm*' -type f 2>/dev/null | head -1)

# Generate php-fpm config if default pool not configured
PHP_FPM_CONF="/etc/php/7.4/fpm/php-fpm.conf"
if [ ! -f "$PHP_FPM_CONF" ]; then
    for ver in 8.0 7.4 7.3 7.2 7.1 7.0; do
        if [ -f "/etc/php/$ver/fpm/php-fpm.conf" ]; then
            PHP_FPM_CONF="/etc/php/$ver/fpm/php-fpm.conf"
            break
        fi
    done
fi

# Start php-fpm
if [ -n "$PHP_FPM" ]; then
    $PHP_FPM --daemonize --fpm-config "$PHP_FPM_CONF" 2>/dev/null || true
fi

# Start nginx
exec /usr/local/nginx/sbin/nginx -g 'daemon off;'
