FROM python:3.9.6-slim

ENV APP_ENV production

COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt

COPY ./wsgi.py ./boot.sh /app/
RUN chmod +x /app/boot.sh

COPY ./api /app/api
COPY ./instance /app/instance

WORKDIR /app

RUN useradd cache_api
USER cache_api

EXPOSE 8080

ENTRYPOINT ["bash", "/app/boot.sh"]
