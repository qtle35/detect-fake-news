from factory import app, db
from routes import blueprint
from auth.user import User
from label.label import Label

app.register_blueprint(blueprint)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, label=Label)

if __name__ == "__main__":
    app.run(debug=True)
