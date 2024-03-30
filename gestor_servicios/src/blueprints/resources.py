from flask import request, Blueprint
from flask.json import jsonify
from commands.notificaciones import CrearNotificaiconMasiva
from commands.registrar import RegistrarServicio

servicios_blueprint = Blueprint('servicios', __name__)

# Recurso que expone la funcionalidad healthcheck
@servicios_blueprint.route('/servicios/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone la funcionalidad notificacion Masiva
@servicios_blueprint.route('/servicios/notificacion', methods=['POST'])
def notifiacion_masiva():
    data = request.get_json()
    return CrearNotificaiconMasiva(data).execute()

# Recurso que expone la funcionalidad registro de servicios
@servicios_blueprint.route('/servicios', methods=['POST'])
def registrar_servicio():
    data = request.get_json()
    headers = request.headers
    return RegistrarServicio(data, headers).execute()