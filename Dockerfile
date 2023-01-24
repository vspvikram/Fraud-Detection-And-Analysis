FROM python:3.9

# ENV MODEL_DIR=/app/models
# ENV MODEL_FILE=xgb_clf.joblib
# ENV AMOUNT_SCALER=amount_scaler.joblib
# ENV TIME_SCALER=time_scaler.joblib

COPY requirements.txt /opt/program/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /opt/program/requirements.txt

ENV PYTHONUNBUFFERED=TRUE
ENV PATH="/opt/program:${PATH}"

COPY /data/train.csv /opt/ml/input/data/training/train.csv
COPY /data/test.csv /opt/ml/input/data/inference/test.csv

COPY train.py /opt/program/train.py
COPY predictor.py /opt/program/predictor.py
COPY serve /opt/program/serve
COPY wsgi.py /opt/program/wsgi.py

WORKDIR /opt/program
