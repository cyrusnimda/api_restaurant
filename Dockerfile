FROM python:3.5-slim

RUN apt-get update && apt-get install -y python3-pip python3-dev libmysqlclient-dev
COPY  . /code
WORKDIR /code
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python", "console.py", "run_api"]
#CMD ["/usr/local/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--access-logfile", "/var/log/api_restaurant.log", "api.main:app"]
