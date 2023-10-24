from flask import Flask
from flask_cors import CORS
from controllers.modelcontroller import controllers_bp
from controllers.maucontroller import controllers_bp1

app = Flask(__name__)
CORS(app)


app.register_blueprint(controllers_bp)
app.register_blueprint(controllers_bp1)

connection = None
if __name__ == "__main__":
    app.run(debug=True)
