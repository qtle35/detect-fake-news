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
    lsLabels = cursor.fetchall()
    lsLabelEntity = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in lsLabels]

    return lsLabelEntity
  except Exception as e:
    print(str(e))
    return None

def getOneLabelById(id):
  conn = create_db_connection()
  if conn:
    cursor = conn.cursor()
  try:
    cursor.execute(f'''SELECT * FROM label WHERE id = {id}''')
    label = cursor.fetchone()
    labelEntity = {'id': label[0], 'name': label[1], 'description': label[2]}
    return labelEntity
  except Exception as e:
    print(str(e))
    return None

def createLabel(label):
  conn = create_db_connection()
  if conn:
    cursor = conn.cursor()
  try:
    cursor.execute('''INSERT INTO label (name, description) VALUES (%s, %s)''',
                    (label.get('name'), label.get('description')))
    conn.commit()

    return True
  except Exception as e:
    print(str(e))
    return False

def deleteLabelById(id):
  conn = create_db_connection()
  if conn:
    cursor = conn.cursor()
  try:
    cursor.execute(f'''DELETE FROM label WHERE id = {id}''')
    conn.commit()

    return True
  except Exception as e:
    print(str(e))
    return False
