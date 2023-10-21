import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mysql.connector
from mysql.connector import Error
from flask import jsonify
from db import create_db_connection, close_db_connection
import os

def getAllLabels():
  conn = create_db_connection()
  if conn:
    cursor = conn.cursor()
  try:
    cursor.execute('''SELECT * FROM label''')
    lsmodel = cursor.fetchall()
    model_list = [{'id': row[0], 'name': row[1], 'date': row[2], 'acc': row[3],
                    'pre': row[4], 're': row[5], 'f1': row[6]} for row in lsmodel]

    return lsmodel
  except Exception as e:
    print(str(e))
    return []

def createLabel(label):
  print(label)
  # conn = create_db_connection()
  # if conn:
  #   cursor = conn.cursor()
  # try:
  #   cursor.execute(''' INSERT INTO label (name, description) VALUES (%s, %s)''',
  #                   (name, description))
  #   conn.commit()

  #   return True
  # except Exception as e:
  #   print(str(e))
  #   return False
  return True

