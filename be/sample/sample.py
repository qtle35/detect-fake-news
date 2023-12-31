from factory import db
from flask import jsonify
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT, DATE
import csv
from label.label import Label
from sqlalchemy import text
import json
from sqlalchemy.orm import contains_eager
from sqlalchemy import update, func
from io import StringIO


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

    def getSamples():
        samples = Sample.query.all()
        list_sample = []
        for sample in samples:
            sample_dict = sample.__dict__
            sample_dict['ngayTaoMau'] = sample.ngayTaoMau.__str__()
            sample_dict['ngaySuaMau'] = sample.ngaySuaMau.__str__()
            if sample.label != None:
                sample_dict['nhan_id'] = sample.label.id
                sample_dict['nhan_name'] = sample.label.name
                sample_dict.pop('label')
            sample_dict.pop('_sa_instance_state')
            list_sample.append(sample.__dict__)
        return list_sample

    def getAllSamples(page=1, per_page=10, offset=0):
        try:
            page = max(1, page)  # Ensure page is always at least 1
            offset = (page - 1) * per_page
            stmt = (
                db.select(Sample)
                .outerjoin(Sample.label)
                .order_by(Sample.id)
                .offset(offset)
                .limit(per_page)
            )
            list_sample_dict = []
            for row in db.session.execute(stmt):
                sample_dict = row.Sample.__dict__
                sample_dict['ngayTaoMau'] = row.Sample.ngayTaoMau.__str__()
                sample_dict['ngaySuaMau'] = row.Sample.ngaySuaMau.__str__()
                if row.Sample.label != None:
                    sample_dict['nhan_id'] = row.Sample.label.id
                    sample_dict['nhan_name'] = row.Sample.label.name
                    sample_dict.pop('label')
                sample_dict.pop('_sa_instance_state')
                list_sample_dict.append(sample_dict)
                # break
            return list_sample_dict
        except Exception as e:
            print("Error executing SQL query:", str(e))
            return None

    def searchSamplesByTitle(title, page, per_page, offset):
        try:
            stmt = (
                db.select(Sample)
                .filter(Sample.title.ilike(f"%{title}%"))
                .outerjoin(Sample.label)
                .order_by(Sample.id)
                .offset(offset)
                .limit(per_page)
            )
            list_sample_dict = []
            for row in db.session.execute(stmt):
                sample_dict = row.Sample.__dict__
                sample_dict['ngayTaoMau'] = row.Sample.ngayTaoMau.__str__()
                sample_dict['ngaySuaMau'] = row.Sample.ngaySuaMau.__str__()
                if row.Sample.label != None:
                    sample_dict['nhan_id'] = row.Sample.label.id
                    sample_dict['nhan_name'] = row.Sample.label.name
                    sample_dict.pop('label')
                sample_dict.pop('_sa_instance_state')
                list_sample_dict.append(sample_dict)
                # break
            return list_sample_dict
        except Exception as e:
            print("Error executing SQL query:", str(e))
            return None

    def countSamplesByTitle(title):
        try:
            count = Sample.query.filter(
                Sample.title.ilike(f"%{title}%")).count()
            return count
        except Exception as e:
            print("Error executing SQL query:", str(e))
            return 0

    def getOneSampleById(id):
        sample = Sample.query.get(id)
        sample_dict = sample.__dict__
        if sample.label != None:
            sample_dict['nhan_id'] = sample.label.id
            sample_dict['nhan_name'] = sample.label.name
            sample_dict.pop('label')
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
            #     csv_writer.writerow([sample.get('title'), sample.get('noiDung'), sample.get(
            #         'theLoai'), sample.get('ngayTaoMau'), sample.get('nhan_id')])
            # Sample.query.add_entity(sample)
            return True
        except Exception:
            return False

    def updateSample(id, sample):
        try:
            new_sample = Sample.query.get(id)
            new_sample.title = sample.get('title')
            new_sample.noiDung = sample.get('noiDung')
            new_sample.theLoai = sample.get('theLoai')
            new_sample.ngayTaoMau = sample.get('ngayTaoMau')
            new_sample.ngaySuaMau = sample.get('ngaySuaMau')
            new_sample.isnew = sample.get('isnew')
            new_sample.nhan_id = sample.get('nhan_id')

            db.session.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def deleteSampleById(id):
        sample = Sample.query.get(id)
        if not sample:
            return False

        try:
            db.session.delete(sample)
            db.session.commit()
            data_to_remove = [sample.title, sample.noiDung, sample.theLoai]
            # with open('train.csv', 'r', newline='', encoding='utf-8') as csvfile, StringIO() as temp_file:
            #     csv_reader = csv.reader(csvfile)
            #     csv_writer = csv.writer(temp_file)

            #     for row in csv_reader:
            #         if data_to_remove != row[0:3]:  # So sánh các thông tin
            #             csv_writer.writerow(row)

            #     # Ghi lại dữ liệu đã lọc vào tệp CSV
            #     with open('train.csv', 'w', newline='', encoding='utf-8') as new_csvfile:
            #         new_csvfile.write(temp_file.getvalue())

            return True
        except Exception as e:
            print(str(e))
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
    def set_isnew_to_null_select(ids):
        try:
            stmt = update(Sample).where(Sample.id.in_(ids)).values(isnew=None)
            db.session.execute(stmt)
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
