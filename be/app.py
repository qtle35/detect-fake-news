from flask import Flask
from flask_cors import CORS
from config import ApplicationConfig
import models.label as label
from controllers.modelcontroller import controllers_bp

app = Flask(__name__)
CORS(app)
app.config.from_object(ApplicationConfig)
label.db.init_app(app)

with app.app_context():
    label.db.create_all()


app.register_blueprint(controllers_bp)

connection = None
if __name__ == "__main__":
    app.run(debug=True)
