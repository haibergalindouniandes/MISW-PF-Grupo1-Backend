# Importación de dependencias
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from blueprints.resources import consultas_blueprint
from errors.errors import ApiError
from models.models import db
import logging
import os

# Configuración logger
logging.basicConfig(level=logging.INFO)

# Constantes
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME =  os.environ["DB_NAME"]
APP_PORT =  int(os.getenv("APP_PORT", default=3000))

# Configuracion app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.register_blueprint(consultas_blueprint)
app_context = app.app_context()
cors = CORS(app)
app_context.push()
db.init_app(app)
api = Api(app)


# Manejador de errores
@app.errorhandler(ApiError)
def handle_exception(err): # pragma: no cover
    response = {
        "msg": err.description,
    }
    return jsonify(response), err.code

if __name__ == "__main__": # pragma: no cover
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=APP_PORT)
