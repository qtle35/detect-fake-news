import pandas as pd
import numpy as np
from flask import jsonify, request
from routes import blueprint
from model.model import Model
from sample.sample import Sample
from predict_log.predict_log import PredictLog
import json
from factory import auth
from sklearn.model_selection import train_test_split


@blueprint.route('/getdatacount', methods=['GET'])
def checktrain():
    dataCount = Sample.getDataCount()
    return jsonify(dataCount), 200


@blueprint.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text')
    id = data.get('model')
    prediction = Model.predic(text, id)
    PredictLog.createPredictLog(
        text, id, 'Fake' if prediction[0] == 0 else 'Real')
    if (prediction[0] == 0):
        output = "Unreliable"
    else:
        output = "Reliable"
    return jsonify({'prediction': output}), 200


@blueprint.route('/retrain', methods=['POST'])
def retrain():
    data = request.json
    # print(data)
    selected = data
    ids = []
    X = []
    y = []
    print('1111111')
    print(len(selected))
    print('1111')
    for item in selected:
        X.append(item['noiDung'])
        label = item['label']['id']
        y.append(label)
        ids.append(item['id'])
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    Sample.set_isnew_to_null_select(ids)
    # df_train = pd.read_csv('train.csv')
    # df_test = pd.read_csv('test.csv')
    # x_train = df_train['text']
    # y_train = df_train['label']
    # x_test = df_test['text']
    # y_test = df_test['label']
    Model.trainData(x_train, x_test, y_train, y_test)
    return '1', 200


@blueprint.route('/getmodel', methods=['GET'])
def getmodel():
    return json.dumps(Model.getModels())


@blueprint.route('/deletemodel', methods=['POST'])
def deletemodel():
    if Model.deleteModel(request.json.get('model')):
        return '1', 200
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/model-stat', methods=['GET'])
def statModel():
    name = request.args.get('name')
    startTime = request.args.get('start-time')
    endTime = request.args.get('end-time')
    if not name or not startTime or not endTime:
        return jsonify({'message': 'Error'}), 400
    return json.dumps(Model.getModelStat(name, startTime, endTime)), 200
    # '2023-11-07 21:44:46'
