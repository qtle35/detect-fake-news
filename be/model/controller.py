import pandas as pd
from flask import jsonify, request
from routes import blueprint
from model.model import Model
import json
from factory import auth

@blueprint.route('/getdatacount', methods=['GET'])
def checktrain():
    dataCount = Model.getDataCount()
    return jsonify(dataCount), 200

@blueprint.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text')
    url = data.get('model')
    prediction = Model.predic(text,url)
    if (prediction[0] == 0):
        output = "Unreliable"
    else:
        output = "Reliable"
    return jsonify({'prediction': output}), 200

@blueprint.route('/retrain', methods=['GET'])
def retrain():
    data = request.json
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