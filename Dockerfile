#
#
#

FROM python:3.8-alpine
WORKDIR /code

# not for deploy
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

#RUN apk update
#RUN apk add postgresql-client

RUN pip3 install -r requirements.txt
