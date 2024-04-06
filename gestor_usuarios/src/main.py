# Importación de dependencias
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from blueprints.resources import usuarios_blueprint
from errors.errors import ApiError
from models.models import db
import logging
import os
from flask_jwt_extended import JWTManager


# Configuración logger
logging.basicConfig(level=logging.INFO)

# Constantes
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME =  os.environ["DB_NAME"]
JWT_SECRET_KEY =  os.environ["JWT_SECRET_KEY"]
APP_PORT =  int(os.getenv("APP_PORT", default=3000))

# Configuracion app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.register_blueprint(usuarios_blueprint)
app_context = app.app_context()
app_context.push()
cors = CORS(app)
db.init_app(app)
db.create_all()
api = Api(app)
jwt = JWTManager(app)

# Manejador de errores
@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description,
    }
    return jsonify(response), err.code

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)