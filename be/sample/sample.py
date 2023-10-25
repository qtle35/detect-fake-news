from factory import db
from flask import jsonify
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT, DATE

class Sample(db.Model):
    __tablename__ = "sample"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(LONGTEXT)
    content = db.Column(LONGTEXT)
    category = db.Column(LONGTEXT)
    create_at = db.Column(DATE)
    update_at = db.Column(DATE)
    is_new = db.Column(TINYINT)
    label_id = db.Column(db.Integer, db.ForeignKey("label.id"))
    label = db.relationship("Label", back_populates="samples")

    def getAllSamples():
        samples = Sample.query.all()
        list_sample_dict = []
        for sample in samples:
            sample.__dict__['create_at'] = sample.create_at.strftime('%Y-%m-%d')
            sample.__dict__['update_at'] = sample.update_at.strftime('%Y-%m-%d')
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
                                content=sample.get('content'),
                                category=sample.get('category'),
                                create_at=sample.get('create_at'),
                                update_at=sample.get('update_at'),
                                is_new=sample.get('is_new'),
                                label_id=sample.get('label_id'))
            db.session.add(new_sample)
            db.session.commit()
            # Sample.query.add_entity(sample)
            return True
        except Exception:
            return False

    def updateSample(id, sample):
        try:
            new_sample = Sample.query.get(id)
            new_sample.title=sample.get('title') 
            new_sample.content=sample.get('content')
            new_sample.category=sample.get('category')
            new_sample.create_at=sample.get('create_at')
            new_sample.update_at=sample.get('update_at')
            new_sample.is_new=sample.get('is_new')
            new_sample.label_id=sample.get('label_id')

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
