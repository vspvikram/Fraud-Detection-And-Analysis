FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget \
    nginx \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

COPY requirements.txt /opt/program/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/program/requirements.txt
RUN pip3 install gevent gunicorn

ENV PYTHONUNBUFFERED=TRUE
ENV PATH="/opt/program:${PATH}"

RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/output
RUN mkdir -p /opt/ml/scalers

COPY /data/train.csv /opt/ml/input/data/training/train.csv
COPY /data/test.csv /opt/ml/input/data/inference/test.csv
COPY /data/test_copy.csv /opt/ml/input/data/inference/test_copy.csv

COPY train /opt/program/train
COPY predictor.py /opt/program/predictor.py
COPY serve /opt/program/serve
COPY wsgi.py /opt/program/wsgi.py
COPY nginx.conf /opt/program/nginx.conf

WORKDIR /opt/program
RUN python train
