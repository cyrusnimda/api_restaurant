FROM debian:stretch-slim
MAINTAINER Josu Ruiz <josu@ontro.co.uk>

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    mysql-client \
    default-libmysqlclient-dev

WORKDIR /var/www/html/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN export PATH=${PATH}:/usr/lib/python3/dist-packages

ENV SERVER_ENV=Development
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile /var/log/api_restaurant.log api.main:app
#CMD [ "gunicorn", "-c", "/var/www/html/gunicorn.conf", "api.main:app" ]
