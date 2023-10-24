from flask import jsonify, request, Blueprint
from services.mauservice import getMaus, getMau, saveMau, updateMau, deleteMau

controllers_bp1 = Blueprint('controller_bp1', __name__)

@controllers_bp1.route('/maus', methods=['GET'])
def get_maus():
    mau_list = getMaus()
    return jsonify(mau_list)

@controllers_bp1.route('/maus/<int:mau_id>', methods=['GET'])
def get_mau(mau_id):
    mau_info = getMau(mau_id)
    if mau_info:
        return jsonify(mau_info)
    return jsonify({"error": "Không tìm thấy mẫu với ID đã cho"}), 404

@controllers_bp1.route('/maus/save', methods=['POST'])
def save_mau():
    data = request.json
    title = data.get('title')
    noiDung = data.get('noiDung')
    theLoai = data.get('theLoai')
    idNhan = data.get('nhan_id')
    ngayTaoMau = data.get('ngayTaoMau')
    ngaySuaMau = data.get('ngaySuaMau')

    saveMau(title, noiDung, theLoai, idNhan, ngayTaoMau, ngaySuaMau)
    response_data = {
        "message": "Mẫu đã được lưu thành công!",
        "ngayTaoMau": ngayTaoMau,
        "ngaySuaMau": ngaySuaMau
    }
    return jsonify(response_data)

@controllers_bp1.route('/maus/update/<int:mau_id>', methods=['PUT'])
def update_mau(mau_id):
    data = request.json
    # mau_id = data.get('mau_id') 
    title = data.get('title')
    noiDung = data.get('noiDung')
    theLoai = data.get('theLoai')
    nhan_id = data.get('nhan_id')
    ngaySuaMau = data.get('ngaySuaMau')

    updateMau(mau_id, title, noiDung, theLoai, nhan_id,ngaySuaMau)
    response_data = {
        "message": "Mẫu đã được cập nhật thành công!",
        "ngaySuaMau": ngaySuaMau
    }
    print(ngaySuaMau)
    return jsonify(response_data)

@controllers_bp1.route('/maus/delete/<int:mau_id>', methods=['DELETE'])
def delete_mau(mau_id):
    # data = request.json
    # mau_id = data.get('mau_id')
    deleteMau(mau_id)
    return jsonify({"message": "Mẫu đã được xóa thành công!"})
