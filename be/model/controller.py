import pandas as pd
import numpy as np
from flask import jsonify, request
from routes import blueprint
from model.model import Model
from sample.sample import Sample
from predict_log.predict_log import PredictLog
import json
from factory import auth

@blueprint.route('/getdatacount', methods=['GET'])
def checktrain():
    dataCount = Sample.getDataCount()
    return jsonify(dataCount), 200

@blueprint.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text')
    url = data.get('model')
    prediction, probability = Model.predic(text,url)
    PredictLog.createPredictLog(text, url, 'Fake' if prediction[0] == 0 else 'Real', float(np.max(probability)))
    if (prediction[0] == 0):
        output = "Unreliable"
    else:
        output = "Reliable"
    return jsonify({'prediction': output}), 200

@blueprint.route('/retrain', methods=['POST'])
def retrain():
    data = request.json
    print('--------------------------------')
    print(data)
    text = data.get('time')
    df_train = pd.read_csv('train.csv')
    df_test = pd.read_csv('test.csv')
    x_train = df_train['text']
    y_train = df_train['label']
    x_test = df_test['text']
    y_test = df_test['label']
    Model.trainData(x_train, x_test, y_train, y_test, text)
    return '1', 200
@blueprint.route('/getmodel', methods=['GET'])
def getmodel():
    return json.dumps(Model.getModels())
@blueprint.route('/deletemodel', methods=['POST'])
def deletemodel():
    if Model.deleteModel(request.json.get('model')):
        return '1', 200
    return jsonify({'message': 'Error'}), 400