from flask import request, Blueprint
from commands.alertas import CrearAlerta
from flask.json import jsonify

from utilities.utilities import formatDateTimeToUTC

entrenamientos_blueprint = Blueprint('entrenamientos', __name__)

# Recurso que expone la funcionalidad healthcheck
@entrenamientos_blueprint.route('/entrenamientos/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone la funcionalidad notificacion de Alerta
@entrenamientos_blueprint.route('/entrenamientos/alerta', methods=['POST'])
def notifiacion_alerta():
    #TODO: Agregar validacion de Token
    data = request.get_json()
    return CrearAlerta(data).execute()