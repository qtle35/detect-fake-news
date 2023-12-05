from flask import jsonify, request
from routes import blueprint
from label.label import labels_schema, label_schema
from label.service import LabelService
import json
from factory import auth

@blueprint.route('/label/all', methods=['GET'])
@auth.login_required
def getAllLabels():
    return labels_schema.dump(LabelService.getAllLabels())

@blueprint.route('/label', methods=['GET'])
@auth.login_required
def getLabels():
    search = request.args.get('search')
    return labels_schema.dump(LabelService.getLabels(search))

@blueprint.route('/label/<id>', methods=['GET'])
@auth.login_required
def getLabel(id):
    return label_schema.dump(LabelService.getOneLabelById(id))

@blueprint.route('/label/new', methods=['POST'])
@auth.login_required
def createLabel():
    label = label_schema.load(request.json)
    if LabelService.createLabel(label):
        return jsonify({'message': 'Created'}), 201
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/label', methods=['PUT'])
@auth.login_required
def updateLabel():
    label = label_schema.load(request.json)
    if LabelService.updateLabel(label):
        return jsonify({'message': 'Updated'}), 200
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/label/<id>', methods=['DELETE'])
@auth.login_required
def deleteLabel(id):
    if LabelService.deleteLabelById(id):
        return jsonify({'message': 'Deleted'}), 200
    return jsonify({'message': 'Error'}), 400
