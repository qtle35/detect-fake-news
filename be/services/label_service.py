from flask import jsonify
from label.label import Label
from factory import db

def getAllLabels():
  labels = Label.query.all()
  list_label_dict = []
  for label in labels:
    label.__dict__.pop('_sa_instance_state') 
    list_label_dict.append(label.__dict__)
  return list_label_dict

def getOneLabelById(id):
  label = Label.query.get(id)
  label_dict = label.__dict__
  label_dict.pop('_sa_instance_state')
  return label_dict

def createLabel(label):
  try:
    new_label = Label(name=label.get('name'), description=label.get('description'))
    db.session.add(new_label)
    db.session.commit()
    # Label.query.add_entity(label)
    return True
  except Exception:
    return False

def updateLabel(id, label):
  try:
    new_label = Label.query.get(id)
    new_label.name = label.get('name')
    new_label.description = label.get('description')

    db.session.commit()
    return True
  except Exception as e:
    print(str(e))
    return False

def deleteLabelById(id):
  try:
    label = Label.query.get(id)
    db.session.delete(label)
    db.session.commit()
    return True
  except Exception:
    return False
