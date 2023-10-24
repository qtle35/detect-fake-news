from flask import Flask
from flask_cors import CORS
from controllers.modelcontroller import controllers_bp
from controllers.maucontroller import controllers_bp1
from controllers.labelcontroller import controllers_bp2

app = Flask(__name__)
CORS(app)


app.register_blueprint(controllers_bp)
app.register_blueprint(controllers_bp1)
app.register_blueprint(controllers_bp2)

connection = None
if __name__ == "__main__":
    app.run(debug=True)
