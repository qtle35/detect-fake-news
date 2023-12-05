from label.label import Label
from factory import db

class LabelService:
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
    if not LabelService.getOneLabelById(id):
      return False
    try:
      label = Label.query.get(id)
      db.session.delete(label)
      db.session.commit()
      return True
    except Exception:
      return False