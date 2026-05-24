FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       apache2 \
       php \
       libapache2-mod-php \
       php-cli \
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod php8.3

WORKDIR /var/www/html

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]
