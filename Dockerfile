# pull official base image
FROM python:3.8-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variable
# 이 환경변수는 컨테이너의 환경변수
ENV PTYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/
RUN apt-get update
RUN apt-get install -y gcc default-libmysqlclient-dev python-dev
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
