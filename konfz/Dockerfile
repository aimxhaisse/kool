FROM orchardup/python:2.7
MAINTAINER s. rannou <mxs@sbrk.org>

ADD . /code
WORKDIR /code
RUN pip install -r /code/requirements.txt
CMD python koolz.py
