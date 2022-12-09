# pull official base image
FROM python:3.8-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variable
ENV PTYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/
RUN apt-get update
RUN apt-get install -y gcc default-libmysqlclient-dev python-dev vim systemd
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

