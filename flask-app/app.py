# app.py
from flask import Flask
from flask_cors import CORS
from controllers.modelcontroller import controllers_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(controllers_bp)
if __name__ == "__main__":
    app.run(debug=True)
