from factory import db
from flask import jsonify
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT, DATE
import csv
from label.label import Label
from sqlalchemy import text
import json
from sqlalchemy.orm import contains_eager,joinedload

class Sample(db.Model):
    __tablename__ = "mau"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(LONGTEXT)
    noiDung = db.Column(LONGTEXT)
    theLoai = db.Column(LONGTEXT)
    ngayTaoMau = db.Column(DATE)
    ngaySuaMau = db.Column(DATE)
    isnew = db.Column(TINYINT)
    nhan_id = db.Column(db.Integer, db.ForeignKey("label.id"))
    # label = db.relationship("Label", back_populates="samples")
    label = db.relationship("Label", lazy="joined")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def getAllSamples(page=1, per_page=10, offset=0):
        try:
            page = max(1, page)  # Ensure page is always at least 1

            offset = (page - 1) * per_page
            samples = Sample.query \
                .join(Sample.label) \
                .options(contains_eager(Sample.label)) \
                .order_by(Sample.id) \
                .offset(offset) \
                .limit(per_page) \
                .all()
            list_sample_dict = []
            for sample in samples:
                sample_dict = sample.as_dict()
                sample_dict['ngayTaoMau'] = sample.ngayTaoMau.__str__()
                sample_dict['ngaySuaMau'] = sample.ngaySuaMau.__str__()
                sample_dict['nhan_id'] = sample.label.id
                sample_dict['nhan_name'] = sample.label.name
                list_sample_dict.append(sample_dict)
            return list_sample_dict
        except Exception as e:
            print("Error executing SQL query:", str(e))
            return None

    def searchSamplesByTitle(title, page, per_page, offset):
        try:
            samples = Sample.query.filter(Sample.title.ilike(f"%{title}%")) \
                .order_by(Sample.id) \
                .offset(offset) \
                .limit(per_page) \
                .all()
            # Chuyển đổi kết quả thành danh sách từ điển và trả về
            list_sample_dict = []
            for sample in samples:
                sample_dict = sample.as_dict()
                sample_dict['ngayTaoMau'] = sample.ngayTaoMau.__str__()
                sample_dict['ngaySuaMau'] = sample.ngaySuaMau.__str__()
                sample_dict['nhan_id'] = sample.label.id
                sample_dict['nhan_name'] = sample.label.name
                list_sample_dict.append(sample_dict)
            return list_sample_dict
        except Exception as e:
            print("Error executing SQL query:", str(e))
            return None

    def countSamplesByTitle(title):
        try:
            count = Sample.query.filter(Sample.title.ilike(f"%{title}%")).count()
            return count
        except Exception as e:
            print("Error executing SQL query:", str(e))
            return 0

    def getOneSampleById(id):
        sample = Sample.query.get(id)
        sample_dict = sample.__dict__
        sample_dict.pop('_sa_instance_state')
        return sample_dict

    def createSample(sample):
        try:
            new_sample = Sample(title=sample.get('title'), 
                                noiDung=sample.get('noiDung'),
                                theLoai=sample.get('theLoai'),
                                ngayTaoMau=sample.get('ngayTaoMau'),
                                ngaySuaMau=sample.get('ngaySuaMau'),
                                isnew=1,
                                nhan_id=sample.get('nhan_id'))
            db.session.add(new_sample)
            db.session.commit()
            # with open('train.csv', 'a', newline='') as csvfile:
            #     csv_writer = csv.writer(csvfile)
            #     csv_writer.writerow([sample.get('title'), sample.get('noiDung'), sample.get('theLoai'), sample.get('ngayTaoMau'), sample.get('nhan_id')])
            # Sample.query.add_entity(sample)
            return True
        except Exception:
            return False

    def updateSample(id, sample):
        try:
            new_sample = Sample.query.get(id)
            new_sample.title=sample.get('title') 
            new_sample.noiDung=sample.get('noiDung')
            new_sample.theLoai=sample.get('theLoai')
            new_sample.ngayTaoMau=sample.get('ngayTaoMau')
            new_sample.ngaySuaMau=sample.get('ngaySuaMau')
            new_sample.isnew=sample.get('isnew')
            new_sample.nhan_id=sample.get('nhan_id')

            db.session.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def deleteSampleById(id):
        if not Sample.getOneSampleById(id):
            return False
        try:
            sample = Sample.query.get(id)
            db.session.delete(sample)
            db.session.commit()
            return True
        except Exception:
            return False

    def set_isnew_to_null():
        try:
            update_stmt = update(Sample).values(isnew=None)
            db.session.execute(update_stmt)
            db.session.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def getDataCount():
        try:
            count_null = db.session.query(Sample).filter_by(isnew=None).count()
            count_1 = db.session.query(Sample).filter_by(isnew=1).count()
            return {'total': count_null, 'new': count_1}
        except Exception as e:
            print("Error executing SQL query:", str(e))
            return None
        
    # def searchSamplesByTitle(title):
    #     try:
    #         samples = Sample.query.filter(Sample.title.ilike(f"%{title}%")).all()
    #         result = []
    #         for sample in samples:
    #             sample_dict = sample.as_dict()
    #             sample_dict['ngayTaoMau'] = sample.ngayTaoMau.__str__()
    #             sample_dict['ngaySuaMau'] = sample.ngaySuaMau.__str__()
    #             sample_dict['nhan_id'] = sample.label.id
    #             sample_dict['nhan_name'] = sample.label.name
    #             result.append(sample_dict)
    #         return result
    #     except Exception as e:
    #         print("Error executing SQL query:", str(e))
    #         return None




