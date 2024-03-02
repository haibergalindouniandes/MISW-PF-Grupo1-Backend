from flask import request, Blueprint
from flask.json import jsonify
from commands.notificaciones import CrearNotificaiconMasiva
from utilities.utilities import formatDateTimeToUTC

servicios_blueprint = Blueprint('servicios', __name__)

# Recurso que expone la funcionalidad healthcheck
@servicios_blueprint.route('/servicios/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone la funcionalidad notificacion Masiva
@servicios_blueprint.route('/servicios/notificacion', methods=['POST'])
def notifiacion_masiva():
    #TODO: Agregar validacion de Token
    data = request.get_json()
    return CrearNotificaiconMasiva(data).execute()