FROM tiangolo/uwsgi-nginx:python3.8

# Netcat used to check is Postrgreee started
RUN apt-get update && apt-get install -y netcat

ENV LISTEN_PORT 8080

EXPOSE 8080

COPY ./app /app

COPY ./app/custom.conf /etc/nginx/conf.d/custom.conf

COPY ./drugstore /app/drugstore

RUN pip install -r /app/drugstore/requirements.txt

WORKDIR /app/drugstore

