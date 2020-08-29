#
#
#

FROM python:3.8-alpine
WORKDIR /code

# not for deploy
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apk update
RUN apk add bash
RUN apk add postgresql-client
RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  pip3 install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

