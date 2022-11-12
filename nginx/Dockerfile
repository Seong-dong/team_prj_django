FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
RUN apt-get upgrade
RUN apt-get install -y vim
COPY nginx.conf /etc/nginx/conf.d/