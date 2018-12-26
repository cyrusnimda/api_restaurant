FROM debian:stretch-slim
MAINTAINER Josu Ruiz <josu@ontro.co.uk>

RUN apt-get update && apt-get install -y \
    nginx \
    python3 \
    python3-pip \
    mysql-client \
    default-libmysqlclient-dev

# Use our nginx config, not default one.
COPY nginx.conf /etc/nginx/sites-available/default

WORKDIR /var/www/html/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN export PATH=${PATH}:/usr/lib/python3/dist-packages
ENV SERVER_ENV=Development

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

#RUN gunicorn -w 4 -b 127.0.0.1:5000 --access-logfile /var/log/api_restaurant.log api.main:app --daemon

CMD nginx -g "daemon off;"
