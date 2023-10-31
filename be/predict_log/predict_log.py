from factory import db
from flask import jsonify
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT, DATE
import datetime

class PredictLog(db.Model):
  __tablename__ = "predict_log"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  text = db.Column(LONGTEXT, nullable=False)
  model_used = db.Column(db.String(255), nullable=False)
  prediction = db.Column(db.String(255), nullable=False)
  probability = db.Column(db.Double, nullable=False)
  create_at = db.Column(DATE, nullable=False, default=datetime.datetime.now)

  def getAllPredict_logs():
    predict_logs = PredictLog.query.all()
    list_predict_log_dict = []
    for predict_log in predict_logs:
        predict_log.__dict__.pop('_sa_instance_state')
        predict_log.__dict__['create_at'] = str(predict_log.create_at)
        list_predict_log_dict.append(predict_log.__dict__)
    return list_predict_log_dict

  def createPredictLog(text, model_used, prediction, probability):
    try:
      new_predictLog = PredictLog(text=text, 
                                  model_used=model_used,
                                  prediction=prediction,
                                  probability=probability)
      db.session.add(new_predictLog)
      db.session.commit()
      # PredictLog.query.add_entity(predictLog)
      return True
    except Exception:
      return False