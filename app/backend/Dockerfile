FROM python:3.6-alpine

LABEL Author Alessio Rossotti "alessiorossotti@gmail.com"

RUN mkdir /app

COPY requirements.txt /app

# set the working directory in the container to /app
WORKDIR /app

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . /app

ENV FLASK_APP=backend_server.py
CMD flask run -h 0.0.0.0 -p 5000