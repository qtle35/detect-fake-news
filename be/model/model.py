import joblib
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from factory import db, tfidf_vectorizer
from flask import jsonify
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT, DATE
from sqlalchemy import update, func
from sample.sample import Sample
from sqlalchemy.orm import aliased
import os
import datetime

class Model(db.Model):
    __tablename__ = "model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    acc = db.Column(db.Double, nullable=False)
    pre = db.Column(db.Double, nullable=False)
    re = db.Column(db.Double, nullable=False)
    f1 = db.Column(db.Double, nullable=False)
    url_model = db.Column(db.String(255), nullable=False)
    url_tfidf = db.Column(db.String(255), nullable=False)
    # total_sample_train = db.Column(db.Integer, nullable=False)

    def getModels():
        models = Model.query.all()
        list_model_dict = []
        for model in models:
            model.__dict__.pop('_sa_instance_state') 
            list_model_dict.append(model.__dict__)
        return list_model_dict

    def deleteModel(model):
        model_get = Model.query.get(model['id'])
        
        if not model:
            return False
        try:
            db.session.delete(model_get)
            db.session.commit()
            name = f"{model['name']} {model['date']}"
            name = name.replace(' ', '_').replace(':', '')
            model_filename = model['url_model']
            if os.path.exists(model_filename):
                os.remove(model_filename)
            return True
        except Exception:
            return False

    def predic(text, id):
        model_get = Model.query.get(id)
        tfidf_vec = joblib.load(model_get.url_tfidf)
        current_model = joblib.load(model_get.url_model)
        # df = pd.read_csv('train.csv')
        input_vector = tfidf_vec.transform([text])
        prediction = current_model.predict(input_vector)
        return prediction

    def trainData(x_train, x_test, y_train, y_test):
        datetime_now = datetime.datetime.now()
        tfidf = tfidf_vectorizer.fit(x_train)
        joblib.dump(tfidf, f"models/tfidf_{str(datetime_now).replace(':', '').replace(' ', '-')}.pkl")
        # Sample.set_isnew_to_null()
        tfidf_train = tfidf_vectorizer.transform(x_train)
        tfidf_test = tfidf_vectorizer.transform(x_test)
        # Naive Bayes model
        nb_model = MultinomialNB()

        nb_model.fit(tfidf_train, y_train)
        y_pred = nb_model.predict(tfidf_test)
        score = Model.evaluateModel(y_test, y_pred)
        joblib.dump(
            nb_model, f"models/nbmodel_{str(datetime_now).replace(':', '').replace(' ', '-')}.pkl")

        Model.saveModel('nbmodel', datetime_now, score)
        # LogisticRegression model
        lr_model = LogisticRegression(solver='liblinear', random_state=0)
        lr_model.fit(tfidf_train, y_train)
        y_pred = lr_model.predict(tfidf_test)
        score = Model.evaluateModel(y_test, y_pred)
        joblib.dump(
            lr_model, f"models/lrmodel_{str(datetime_now).replace(':', '').replace(' ', '-')}.pkl")
        Model.saveModel('lrmodel', datetime_now, score)
        # PassiveAggressiveClassifier
        pac_model = PassiveAggressiveClassifier(max_iter=50)
        pac_model.fit(tfidf_train, y_train)
        y_pred = pac_model.predict(tfidf_test)
        score = Model.evaluateModel(y_test, y_pred)
        joblib.dump(
            pac_model, f"models/pacmodel_{str(datetime_now).replace(':', '').replace(' ', '-')}.pkl")
        Model.saveModel('pacmodel', datetime_now, score)
        
    def saveModel(name, datetime, score):

        try:
            print(name, datetime, score)
            new_model = Model(name=name, 
                            date=datetime,
                            acc=score['acc'],
                            pre=score['pre'],
                            re=score['re'],
                            f1=score['f1'],
                              url_model=f"models/{name}_{str(datetime).replace(':', '').replace(' ', '-')}.pkl",
                              url_tfidf=f"models/tfidf_{str(datetime).replace(':', '').replace(' ', '-')}.pkl")

            db.session.add(new_model)
            db.session.commit()
            return True
        except Exception:
            return False

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

    