from flask import jsonify, Blueprint
from services.labelservice import getLabels 

controllers_bp2 = Blueprint('controller_bp2', __name__)

@controllers_bp2.route('/labels', methods=['GET'])
def get_labels():
    labels = getLabels()
    # Sửa thành trả về dữ liệu JSON trực tiếp
    return jsonify(labels)
