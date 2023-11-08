from flask import jsonify, request
from routes import blueprint
from sample.sample import Sample
import json  
from factory import auth

# @blueprint.route('/maus', methods=['GET'])
# def getAllSamples():
#     return json.dumps(Sample.getAllSamples())

@blueprint.route('/maus', methods=['GET'])
def getMaus():
    page = request.args.get('page', type=int, default=1)
    per_page = request.args.get('per_page', type=int, default=10)
    offset = (page - 1) * per_page

    search_title = request.args.get('title')

    if search_title:
        # Nếu có tìm kiếm 'title', thực hiện tìm kiếm và trả về kết quả
        maus = Sample.searchSamplesByTitle(search_title, page, per_page, offset)
        total_count = Sample.countSamplesByTitle(search_title)
    else:
        # Nếu không có tìm kiếm, thực hiện truy vấn dữ liệu phân trang
        maus = Sample.getAllSamples(page, per_page, offset)
        total_count = Sample.query.count()

    return jsonify({
        'maus': maus,
        'total_count': total_count
    })

@blueprint.route('/maus/<id>', methods=['GET'])
def getSample(id):
    res = Sample.getOneSampleById(id)
    if not res:
        return jsonify({'message': f'Failed to get sample with id {id}'}), 400
    return jsonify(res)


@blueprint.route('/maus/save', methods=['POST'])
def createSample():
    if Sample.createSample(request.json):
        return jsonify({'message': 'Created'}), 200
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

# @blueprint.route('/maus/search', methods=['GET'])
# def searchSamples():
#     title = request.args.get('title')
#     if not title:
#         return jsonify({'message': 'Title parameter is required'}), 400

#     results = Sample.searchSamplesByTitle(title)
#     if results is not None:
#         return jsonify(results), 200
#     else:
#         return jsonify({'message': 'Error while searching samples'}), 500

@blueprint.route('/getsamples', methods=['GET'])
def getsamples():
    return jsonify(Sample.getSamples())