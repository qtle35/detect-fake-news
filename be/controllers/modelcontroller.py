from flask import jsonify, request, Blueprint
from services.modelservice import predic, trainData, getModels, deleteModel
import pandas as pd
import json

controllers_bp = Blueprint('controller_bp', __name__)

@controllers_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text')
    url = data.get('model')
    prediction = predic(text,url)
    if (prediction[0] == 0):
        output = "Unreliable"
    else:
        output = "Reliable"
    return jsonify({'prediction': output}), 200

@controllers_bp.route('/retrain', methods=['POST'])
def retrain():
    data = request.json
    text = data.get('time')
    df_train = pd.read_csv('train.csv')
    df_test = pd.read_csv('test.csv')
    x_train = df_train['text']
    y_train = df_train['label']
    x_test = df_test['text']
    y_test = df_test['label']
    trainData(x_train, x_test, y_train, y_test, text)
    return '1', 200
@controllers_bp.route('/getmodel', methods=['GET'])
def getmodel():
    models = getModels()
    return jsonify(models), 200
@controllers_bp.route('/deletemodel', methods=['POST'])
def deletemodel():
    model = request.json.get('model')
    print(model)
    deleteModel(model)
    return '1',200