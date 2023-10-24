from flask import jsonify, request
from routes import blueprint
import services.label_service as label_service
import json
from factory import auth

@blueprint.route('/label', methods=['GET'])
@auth.login_required
def getAllLabels():
    return json.dumps(label_service.getAllLabels())

@blueprint.route('/label/<id>', methods=['GET'])
def getLabel(id):
    res = label_service.getOneLabelById(id)
    if not res:
        return jsonify({'message': f'Failed to get label with id {id}'}), 400
    return res

@blueprint.route('/label/new', methods=['POST'])
def createLabel():
    if label_service.createLabel(request.json):
        return jsonify({'message': 'Created'}), 201
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/label/<id>', methods=['PUT'])
def updateLabel(id):
    if label_service.updateLabel(id, request.json):
        return jsonify({'message': 'Updated'}), 200
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/label/<id>', methods=['DELETE'])
def deleteLabel(id):
    if not label_service.getOneLabelById(id):
        return jsonify({'message': 'Not found'}), 404
    if label_service.deleteLabelById(id):
        return '', 204
    return jsonify({'message': 'Error'}), 400
