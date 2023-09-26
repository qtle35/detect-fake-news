
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, request, jsonify
import nltk
import joblib
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS, cross_origin
import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier, LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,  precision_score, recall_score, f1_score, classification_report


app = Flask(__name__)
CORS(app)
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="flask_data"
    )
    if conn.is_connected():
        print("Kết nối đến cơ sở dữ liệu thành công.")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu.")
except Exception as e:
    print(str(e))
cv = CountVectorizer(max_features=5000, ngram_range=(1, 3))
nltk.download('stopwords')
model = joblib.load('model/lrmodel.pkl')
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
df = pd.read_csv('train.csv')
# df.to_sql('news', con=conn, if_exists='replace', index=False)
text_data = df['text'].to_list()
tfidf_vectorizer.fit(text_data)


def input(text):
    input_vector = tfidf_vectorizer.transform([text])
    prediction = model.predict(input_vector)
    print(prediction)
    return prediction


@app.route('/predict', methods=['POST'])
def predict():
    # for rendering results
    # int_features = [x for x in request.form.values()]
    print(request.data)
    data = request.json
    text = data.get('text')
    print('int_features', text)
    prediction = input(text)
    if (prediction[0] == 0):
        output = "Unreliable"
    else:
        output = "Reliable"
    return jsonify({'prediction': output}), 200


# retrain
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
    print(result['acc'])
    print(123)
    return result


def saveModel(name, date, score):
    print(score)
    cursor = conn.cursor()
    try:
        cursor.execute(''' INSERT INTO model (name, date, acc, pre, re, f1) VALUES (%s, %s, %s, %s, %s, %s)''',
                   (name, date, score['acc'], score['pre'], score['re'], score['f1']))
        conn.commit()
    except Exception as e:
        print(str(e))


def trainData(x_train, x_test, y_train, y_test, date):
    tfidf_train = tfidf_vectorizer.fit_transform(x_train)
    tfidf_test = tfidf_vectorizer.transform(x_test)
    # Naive Bayes model
    nb_model = MultinomialNB()
    nb_model.fit(tfidf_train, y_train)
    y_pred = nb_model.predict(tfidf_test)
    score = evaluateModel(y_test, y_pred)
    # joblib.dump(nb_model, "model/nbmodel "+date+".pkl")
    saveModel('nbmodel', date, score)
    # LogisticRegression model
    lr_model = LogisticRegression(solver='liblinear', random_state=0)
    lr_model.fit(tfidf_train, y_train)
    y_pred = lr_model.predict(tfidf_test)
    evaluateModel(y_test, y_pred)
    # joblib.dump(nb_model, "model/lrmodel "+date+".pkl")
    score =  saveModel('lrmodel', date, score)
    # PassiveAggressiveClassifier
    pac_model = PassiveAggressiveClassifier(max_iter=50)
    pac_model.fit(tfidf_train, y_train)
    y_pred = pac_model.predict(tfidf_test)
    score =  evaluateModel(y_test, y_pred)
    # joblib.dump(nb_model, "model/pacmodel "+date+".pkl")
    saveModel('pacmodel', date, score)


@app.route('/retrain', methods=['POST'])
def retrain():
    print(request.data)
    data = request.json
    text = data.get('time')
    df_train = pd.read_csv('train.csv')
    df_test = pd.read_csv('test.csv')
    x_train = df_train['text']
    y_train = df_train['label']
    x_test = df_test['text']
    y_test = df_test['label']
    trainData(x_train, x_test, y_train, y_test, text)
    return '1', 200
from flask import jsonify

@app.route('/getmodel', methods=['GET'])
def getmodel():
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT * FROM model''')
        lsmodel = cursor.fetchall()
        model_list = [{'id':row[0], 'name': row[1], 'date': row[2], 'acc': row[3], 'pre': row[4], 're': row[5], 'f1': row[6]} for row in lsmodel]
        
        return jsonify(model_list), 200
    except Exception as e:
        print(str(e))
        return jsonify([]), 500


if __name__ == "__main__":
    app.run(debug=True)
