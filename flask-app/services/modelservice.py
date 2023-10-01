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

tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
model = None


def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor
    except Error as e:
        print(str(e))
        return None


def getModels():
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor()
    try:
        cursor.execute('''SELECT * FROM model''')
        lsmodel = cursor.fetchall()
        model_list = [{'id': row[0], 'name': row[1], 'date': row[2], 'acc': row[3],
                       'pre': row[4], 're': row[5], 'f1': row[6]} for row in lsmodel]

        return model_list
    except Exception as e:
        print(str(e))
        return []


def saveModel(name, date, score):
    connection = create_db_connection()
    if connection:
        cursor = execute_query(
            connection,
            ''' INSERT INTO model (name, date, acc, pre, re, f1) VALUES (%s, %s, %s, %s, %s, %s)''',
            (name, date, score['acc'], score['pre'], score['re'], score['f1'])
        )
        close_db_connection(connection)


def predic(text, url):
    url = url.replace(' ', '_')
    model = joblib.load(f'model/{url}.pkl')
    df = pd.read_csv('train.csv')
    tfidf_vectorizer.fit(df['text'].to_list())
    input_vector = tfidf_vectorizer.transform([text])
    prediction = model.predict(input_vector)
    return prediction


def evaluateModel(y_test, y_pred):
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    result = {
        'acc': round(accuracy*100, 2),
        'pre': round(precision*100, 2),
        're': round(recall*100, 2),
        'f1': round(f1*100, 2)
    }
    return result


def trainData(x_train, x_test, y_train, y_test, datetime):
    date, time = datetime.split()
    tfidf_train = tfidf_vectorizer.fit_transform(x_train)
    tfidf_test = tfidf_vectorizer.transform(x_test)
    # Naive Bayes model
    nb_model = MultinomialNB()

    nb_model.fit(tfidf_train, y_train)
    y_pred = nb_model.predict(tfidf_test)
    score = evaluateModel(y_test, y_pred)
    joblib.dump(nb_model, f"model/nbmodel_{date}_{time}.pkl")


    saveModel('nbmodel', datetime, score)
    # LogisticRegression model
    lr_model = LogisticRegression(solver='liblinear', random_state=0)
    lr_model.fit(tfidf_train, y_train)
    y_pred = lr_model.predict(tfidf_test)
    score = evaluateModel(y_test, y_pred)
    joblib.dump(lr_model, f"model/lrmodel_{date}_{time}.pkl")
    saveModel('lrmodel', datetime, score)
    # PassiveAggressiveClassifier
    pac_model = PassiveAggressiveClassifier(max_iter=50)
    pac_model.fit(tfidf_train, y_train)
    y_pred = pac_model.predict(tfidf_test)
    score = evaluateModel(y_test, y_pred)
    joblib.dump(pac_model, f"model/pacmodel_{date}_{time}.pkl")
    saveModel('pacmodel', datetime, score)


