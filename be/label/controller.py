from flask import jsonify, request
from routes import blueprint
from label.label import Label
import json
from factory import auth

@blueprint.route('/label/all', methods=['GET'])
@auth.login_required
def getAllLabels():
    return json.dumps(Label.getAllLabels())

@blueprint.route('/label', methods=['GET'])
@auth.login_required
def getLabels():
    search = request.args.get('search')
    return json.dumps(Label.getLabels(search))

@blueprint.route('/label/<id>', methods=['GET'])
@auth.login_required
def getLabel(id):
    res = Label.getOneLabelById(id)
    if not res:
        return jsonify({'message': f'Failed to get label with id {id}'}), 400
    return res

@blueprint.route('/label/new', methods=['POST'])
@auth.login_required
def createLabel():
    if Label.createLabel(request.json):
        return jsonify({'message': 'Created'}), 201
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/label/<id>', methods=['PUT'])
@auth.login_required
def updateLabel(id):
    if Label.updateLabel(id, request.json):
        return jsonify({'message': 'Updated'}), 200
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/label/<id>', methods=['DELETE'])
@auth.login_required
def deleteLabel(id):
    if Label.deleteLabelById(id):
        return jsonify({'message': 'Deleted'}), 200
    return jsonify({'message': 'Error'}), 400
