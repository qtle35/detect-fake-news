from flask import jsonify, request
from routes import blueprint
from sample.sample import Sample
import json
from factory import auth

@blueprint.route('/maus', methods=['GET'])
def getAllSamples():
    return json.dumps(Sample.getAllSamples())

@blueprint.route('/maus/<id>', methods=['GET'])
def getSample(id):
    res = Sample.getOneSampleById(id)
    if not res:
        return jsonify({'message': f'Failed to get sample with id {id}'}), 400
    return res

@blueprint.route('/maus/save', methods=['POST'])
def createSample():
    if Sample.createSample(request.json):
        return jsonify({'message': 'Created'}), 201
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/maus/update/<id>', methods=['PUT'])
def updateSample(id):
    if Sample.updateSample(id, request.json):
        return jsonify({'message': 'Updated'}), 200
    return jsonify({'message': 'Error'}), 400

@blueprint.route('/maus/delete/<id>', methods=['DELETE'])
def deleteSample(id):
    if Sample.deleteSampleById(id):
        return '', 204
    return jsonify({'message': 'Error'}), 400
