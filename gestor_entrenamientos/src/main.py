# Importación de dependencias
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from blueprints.resources import entrenamientos_blueprint
from errors.errors import ApiError
from models.models import db, Entrenamientos
import logging
import json
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
app.register_blueprint(entrenamientos_blueprint)
app_context = app.app_context()
app_context.push()
cors = CORS(app)
db.init_app(app)
db.create_all()
api = Api(app)

# cargar entrenamientos en base de datos
with open('utilities/entrenamientos.json') as fn:
    entrenamientos = json.load(fn)

for rutina, info in entrenamientos.items():
    registro = []
    registro.append(rutina)
    for dato, valor in info.items():
        registro.append(valor)
    print(registro)
    nuevo_entrenamiento = Entrenamientos(rutina=registro[0],
                                         ejercicios=registro[1],
                                         tipo_entrenamiento=registro[2],
                                         proposito=registro[3],
                                         clasificacion=registro[4]
                                         )
    db.session.add(nuevo_entrenamiento)
    db.session.commit()

# Manejador de errores
@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description,
    }
    return jsonify(response), err.code

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=APP_PORT)