from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Label(db.Model):
    __tablename__ = "label"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
