from factory import db, ma
from flask import jsonify

class Label(db.Model):
    __tablename__ = "label"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # samples = db.relationship("Sample", back_populates="label", passive_deletes='all')

    def getAllLabels():
        return Label.query.all()

    def getOneLabelById(id):
        return Label.query.get(id)
    
    def getLabels(search):
        if not search:
            search = ''
        print(Label.query.filter(Label.name.like(f"%{search}%")).all())
        return Label.query.filter(Label.name.like(f"%{search}%")).all()

    def createLabel(label):
        try:
            db.session.add(label)
            db.session.commit()
            return True
        except Exception:
            return False

    def updateLabel(label):
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def deleteLabelById(id):
        if not Label.getOneLabelById(id):
            return False
        try:
            label = Label.query.get(id)
            db.session.delete(label)
            db.session.commit()
            return True
        except Exception:
            return False

class LabelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Label
        load_instance = True

label_schema = LabelSchema()
labels_schema = LabelSchema(many=True)