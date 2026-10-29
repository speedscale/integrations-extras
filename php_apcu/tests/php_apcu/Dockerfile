FROM php:8.3.36-apache-bookworm@sha256:96f820bf68a6e443521586cdd29b9efa1b990df6105b0f8c5524a49492752676

COPY ./src /var/www/html/

RUN pecl install apcu \
  && docker-php-ext-enable apcu

