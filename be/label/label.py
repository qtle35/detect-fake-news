from factory import db, ma
from flask import jsonify

class Label(db.Model):
    __tablename__ = "label"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # samples = db.relationship("Sample", back_populates="label", passive_deletes='all')

class LabelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Label
        load_instance = True

label_schema = LabelSchema()
labels_schema = LabelSchema(many=True)