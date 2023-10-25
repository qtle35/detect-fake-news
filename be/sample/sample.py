from factory import db
from flask import jsonify
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT, DATE
import csv

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
    label = db.relationship("Label", back_populates="samples")

    def getAllSamples():
        samples = Sample.query.all()
        list_sample_dict = []
        for sample in samples:
            sample.__dict__['ngayTaoMau'] = sample.ngayTaoMau.strftime('%Y-%m-%d')
            sample.__dict__['ngaySuaMau'] = sample.ngaySuaMau.strftime('%Y-%m-%d')
            sample.__dict__.pop('_sa_instance_state') 
            list_sample_dict.append(sample.__dict__)
        return list_sample_dict

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
                                isnew=sample.get('isnew'),
                                nhan_id=sample.get('nhan_id'))
            db.session.add(new_sample)
            db.session.commit()
            with open('train.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([title, noiDung, theLoai, ngayTaoMau, nhan_id])
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
