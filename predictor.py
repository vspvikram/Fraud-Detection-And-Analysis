#!/usr/bin/env python3
# predictor.py
# Vikram Singh 12/01/2022

# Environment info
import platform; print(platform.platform())
import numpy; print("Numpy", numpy.__version__)
import sys; print("Python", sys.version)

# Basic libraries
import pandas as pd
import os
from joblib import dump, load

# Others
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
import pickle
import flask
from io import StringIO
import warnings
warnings.filterwarnings("ignore")

# paths of various files in the container
prefix = '/opt/ml/'

input_path = prefix + 'input/data'
output_path = os.path.join(prefix, 'output')
model_path = os.path.join(prefix, 'model')
scalers_path = os.path.join(prefix, 'scalers')

# two channels for the input data
training_channel_name = "training"
training_path = os.path.join(input_path, training_channel_name)

inference_channel_name = "inference"
inference_path = os.path.join(input_path, inference_channel_name)

class ScoringService(object):
    """Class to load the trained model and predict on the input data"""
    model = None
    time_scaler = None
    amount_scaler = None

    @classmethod
    def get_time_scaler(cls):
        """load the time scaler if not already loaded"""
        if cls.time_scaler == None:
            with open(os.path.join(scalers_path, "time-scaler.pkl"), 'rb') as t_file:
                cls.time_scaler = pickle.load(t_file)
        return cls.time_scaler

    @classmethod
    def get_amount_scaler(cls):
        """load the amount scaler if not already loaded"""
        if cls.amount_scaler == None:
            with open(os.path.join(scalers_path, "amount-scaler.pkl"), 'rb') as a_file:
                cls.amount_scaler = pickle.load(a_file)

        return cls.amount_scaler

    @classmethod
    def transform_data(cls, data):
        time_scaler = cls.get_time_scaler()
        amount_scaler = cls.get_amount_scaler()
        if len(data.columns) != 30:
            return -1

        data.iloc[:, 0] = time_scaler.transform(data.iloc[:, 0:1])
        data.iloc[:, 1] = amount_scaler.transform(data.iloc[:, 1:2])

        return data

    @classmethod
    def get_model(cls):
        """load the model and other artifacts if not already loaded"""
        if cls.model == None:
            with open(os.path.join(model_path, "xgboost-model.pkl"), 'rb') as m_file:
                cls.model = pickle.load(m_file)
        return cls.model


    @classmethod
    def predict(cls, data):
        """Predict the classes for the input data in csv/test format"""
        clf = cls.get_model()
        return clf.predict(data)


# starting flask app
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """ Check if the model is avaialble for making the predictions"""
    health = ScoringService.get_model() is not None

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype = 'application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    """ Take a single batch in a csv file and perform prediction on that"""
    data = None 

    # convert from csv to pandas dataframe
    if flask.request.content_type == 'text/csv':
        data = flask.request.data.decode('utf-8')
        s = StringIO(data)
        data = pd.read_csv(s, header=None)
        data = data.iloc[:, 1:]

    else:
        return flask.Response(response="This predictor only supports CSV data", status=415,
                                mimetype="text/plain")

    # transform the data for time and amount features scaling
    data = ScoringService.transform_data(data)
    if not isinstance(data, pd.DataFrame):
        return flask.Response(response="Please provide the correct column format for the data", 
                                status=415, mimetype="text/plain")

    # prediction starts here
    preds = ScoringService.predict(data)

    # changing the np format to csv format
    out = StringIO()
    pd.DataFrame({'results':preds}).to_csv(out, header=False, index=False)
    results = out.getvalue()

    return flask.Response(response=results, status = 200, mimetype="text/csv")



# def inference():
#     # environment variables
#     MODEL_DIR = os.environ["MODEL_DIR"]
#     MODEL_FILE = os.environ["MODEL_FILE"]
#     MODEL_FILE_PATH = os.path.join(MODEL_DIR, MODEL_FILE)

#     TIME_SCALER = os.environ["TIME_SCALER"]
#     TIME_SCALER_PATH = os.path.join(MODEL_DIR, TIME_SCALER)

#     AMOUNT_SCALER = os.environ["AMOUNT_SCALER"]
#     AMOUNT_SCALER_PATH = os.path.join(MODEL_DIR, AMOUNT_SCALER)

#     # loading the training files
#     data = pd.read_csv("./inference.csv")

#     # Loading scalers
#     time_scaler = load(TIME_SCALER_PATH)
#     amount_scaler = load(AMOUNT_SCALER_PATH)

#     data[["Amount"]] = amount_scaler.transform(data[["Amount"]])
#     data[["Time"]] = time_scaler.transform(data[["Time"]])

#     X = data.drop(["Class"], axis=1)
#     y = data["Class"]
#     print("Number of training set samples for each class:")
#     print(y.value_counts())

#     # Loading the model
#     print("Loading the model from: {}".format(MODEL_FILE_PATH))
#     best_estimator = load(MODEL_FILE_PATH)

#     preds = best_estimator.predict(X)
#     preds_proba = best_estimator.predict_proba(X)[:,1]
#     f1_score_ = f1_score(y, preds)
#     recall_ = recall_score(y, preds)
#     precesion_ = precision_score(y, preds)
#     auc_score_ = roc_auc_score(y, preds_proba)

#     print("Recall: {}".format(recall_))
#     print("Precision: {}".format(precesion_))
#     print("f1_score: {}".format(f1_score_))
#     print("roc auc score: {}".format(auc_score_))
    

# if __name__ == "__main__":
#     inference()
