import joblib
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from factory import db, tfidf_vectorizer, tfidf_vec, current_model
from flask import jsonify
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT, DATE
from sqlalchemy import update, func
from sample.sample import Sample
from sqlalchemy.orm import aliased
import os

class Model(db.Model):
    __tablename__ = "model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    acc = db.Column(db.Double, nullable=False)
    pre = db.Column(db.Double, nullable=False)
    re = db.Column(db.Double, nullable=False)
    f1 = db.Column(db.Double, nullable=False)

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
            print(name)
            model_filename = f"models/{name}.pkl"
            if os.path.exists(model_filename):
                os.remove(model_filename)
            return True
        except Exception:
            return False

    def predic(text, url):
        url = url.replace(' ', '_')
        url = url.replace(':', '')
        current_model = joblib.load(f'models/{url}.pkl')
        df = pd.read_csv('train.csv')
        input_vector = tfidf_vec.transform([text])
        prediction = current_model.predict(input_vector)
        return prediction

    def trainData(x_train, x_test, y_train, y_test, datetime):
        date, time = datetime.split()
        time = time.replace(':', '')
        tfidf = tfidf_vectorizer.fit(x_train)
        joblib.dump(tfidf, f"models/tfidf_vec.pkl")
        Model.set_isnew_to_null()
        tfidf_train = tfidf_vectorizer.fit_transform(x_train)
        tfidf_test = tfidf_vectorizer.transform(x_test)
        # Naive Bayes model
        nb_model = MultinomialNB()

        nb_model.fit(tfidf_train, y_train)
        y_pred = nb_model.predict(tfidf_test)
        score = Model.evaluateModel(y_test, y_pred)
        joblib.dump(nb_model, f"models/nbmodel_{date}_{time}.pkl")

        Model.saveModel('nbmodel', datetime, score)
        # LogisticRegression model
        lr_model = LogisticRegression(solver='liblinear', random_state=0)
        lr_model.fit(tfidf_train, y_train)
        y_pred = lr_model.predict(tfidf_test)
        score = Model.evaluateModel(y_test, y_pred)
        joblib.dump(lr_model, f"models/lrmodel_{date}_{time}.pkl")
        Model.saveModel('lrmodel', datetime, score)
        # PassiveAggressiveClassifier
        pac_model = PassiveAggressiveClassifier(max_iter=50)
        pac_model.fit(tfidf_train, y_train)
        y_pred = pac_model.predict(tfidf_test)
        score = Model.evaluateModel(y_test, y_pred)
        joblib.dump(pac_model, f"models/pacmodel_{date}_{time}.pkl")
        Model.saveModel('pacmodel', datetime, score)
        
    def getDataCount():
        try:
            sample_alias = aliased(Sample)
            count_null = db.session.query(func.count(Sample.id)).filter(sample_alias.isnew.is_(None)).scalar()
            count_1 = db.session.query(func.count(Sample.id)).filter(sample_alias.isnew == 1).scalar()
            return {'total': count_null, 'new': count_1}
        except Exception as e:
            print("Error executing SQL query:", str(e))
            return None

    def saveModel(name, date, score):
        try:
            print(name, date, score)
            new_model = Model(name=name, 
                            date=date,
                            acc=score['acc'],
                            pre=score['pre'],
                            re=score['re'],
                            f1=score['f1'])
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

    def set_isnew_to_null():
        try:
            update_stmt = update(Sample).values(isnew=None)
            db.session.execute(update_stmt)
            db.session.commit()
            return True
        except Exception as e:
            print(str(e))
            return False