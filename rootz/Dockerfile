FROM ubuntu:trusty
MAINTAINER s. rannou <mxs@sbrk.org>

RUN apt-get update -qq &&	\
    apt-get -y install nginx &&	\
    apt-get clean

EXPOSE 80

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD rootz.conf /etc/nginx/sites-available/default

CMD nginx
