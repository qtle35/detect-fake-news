
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, request, jsonify
import pickle
import nltk
import pandas as pd
import numpy as np
import joblib
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app)
cv = CountVectorizer(max_features=5000, ngram_range=(1, 3))
nltk.download('stopwords')
model = joblib.load('lrmodel.pkl')
tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)
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
    if(prediction[0] == 0):
        output = "Unreliable"
    else:
        output = "Reliable"
    return jsonify({'prediction': output}), 200


@app.route('/retrain', methods=['POST'])
def retrain():
    print(request.data)
    data = request.json
    text = data.get('time')
    return '1', 200


if __name__ == "__main__":
    app.run(debug=True)
