from factory import app, db
from routes import blueprint
from auth.user import User
from label.label import Label
from sample.sample import Sample
from model.model import Model
from predict_log.predict_log import PredictLog

app.register_blueprint(blueprint)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, label=Label, sample=Sample, model=Model, predict_log=PredictLog)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
