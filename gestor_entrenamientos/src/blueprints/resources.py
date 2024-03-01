from flask import request, Blueprint
from src.commands.alertas import CrearAlerta
from src.commands.plan_entrenamiento import DarPlanEntrenamiento
from flask.json import jsonify

from src.utilities.utilities import formatDateTimeToUTC

entrenamientos_blueprint = Blueprint(name='entrenamientos', import_name=__name__, url_prefix='/entrenamientos')

# Recurso que expone la funcionalidad healthcheck
@entrenamientos_blueprint.route('/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone la funcionalidad notificacion de Alerta
@entrenamientos_blueprint.route('/alerta', methods=['POST'])
def notifiacion_alerta():
    #TODO: Agregar validacion de Token
    data = request.get_json()
    return CrearAlerta(data).execute()

@entrenamientos_blueprint.route('/plan-entrenamiento', methods=['POST'])
def dar_plan_entrenamiento():
    data = request.json()
    return DarPlanEntrenamiento(data)
