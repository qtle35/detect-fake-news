from flask import jsonify, request, Blueprint
from services.modelservice import predic, trainData, getModels, deleteModel, getDataCount
import services.label_service as label_service
import pandas as pd
# from services.mauservice import getDataCount

controllers_bp = Blueprint('controller_bp', __name__)


@controllers_bp.route('/getdatacount', methods=['GET'])
def checktrain():
    print(11111111)
    dataCount = getDataCount()
    print(dataCount)
    return jsonify(dataCount), 200
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


@controllers_bp.route('/label', methods=['GET'])
def getAllLabels():
    return label_service.getAllLabels();

@controllers_bp.route('/label/<id>', methods=['GET'])
def getLabel(id):
    res = label_service.getOneLabelById(id)
    if not res:
        return jsonify({'message': f'Failed to get label with id {id}'}), 400
    return res

@controllers_bp.route('/label/new', methods=['POST'])
def createLabel():
    if label_service.createLabel(request.json):
        return jsonify({'message': 'Created'}), 201
    return jsonify({'message': 'Error'}), 400

@controllers_bp.route('/label/<id>', methods=['POST'])
def updateLabel(id):
    if label_service.updateLabel(id, request.json):
        return jsonify({'message': 'Updated'}), 200
    return jsonify({'message': 'Error'}), 400

@controllers_bp.route('/label/<id>', methods=['DELETE'])
def deleteLabel(id):
    if not label_service.getOneLabelById(id):
        return jsonify({'message': 'Not found'}), 404
    if label_service.deleteLabelById(id):
        return '', 204
    return jsonify({'message': 'Error'}), 400
