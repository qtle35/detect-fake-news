import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import ApplicationConfig
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

app.config.from_object(ApplicationConfig)
db = SQLAlchemy(app)  # , model_class=BaseModel)

with app.app_context():
    db.create_all()

# cors with defaults, which means allow all domains, it is fine for the moment
cors = CORS(app, supports_credentials=True)
bcrypt = Bcrypt()
auth = HTTPBasicAuth()