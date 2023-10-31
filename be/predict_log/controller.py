from flask import jsonify, request
from routes import blueprint
from predict_log.predict_log import PredictLog
import json
from factory import auth

@blueprint.route('/predict-log/all', methods=['GET'])
def getAllPredictLogs():
  return json.dumps(PredictLog.getAllPredict_logs())