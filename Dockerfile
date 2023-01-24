FROM python:3.9-slim

# installing the required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget \
    nginx \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

COPY requirements.txt /opt/program/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/program/requirements.txt
RUN pip3 install gevent gunicorn

# setting up environment variables 
# PYTHONUNBUFFERED keeps python from buffering our standard output stream to deliver the logs to the user quickly
# PATH variable to find the train and serve programs when container is invoked
ENV PYTHONUNBUFFERED=TRUE
ENV PATH="/opt/program:${PATH}"

# creating the model and artifacts folders
RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/output
RUN mkdir -p /opt/ml/scalers

# copy the data files to the container
COPY /data/train.csv /opt/ml/input/data/training/train.csv
COPY /data/test.csv /opt/ml/input/data/inference/test.csv
COPY /data/test_copy.csv /opt/ml/input/data/inference/test_small.csv

# copy the executable files
COPY train /opt/program/train
COPY predictor.py /opt/program/predictor.py
COPY serve /opt/program/serve
COPY wsgi.py /opt/program/wsgi.py
COPY nginx.conf /opt/program/nginx.conf

# defining the work directory for the container image
WORKDIR /opt/program
