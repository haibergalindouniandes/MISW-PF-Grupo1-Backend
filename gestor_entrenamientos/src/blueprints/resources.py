from flask import request, Blueprint
from commands.alertas import CrearAlerta
from commands.plan_entrenamiento import CrearPlanEntrenamiento, DarPlanEntrenamiento
from flask.json import jsonify

from utilities.utilities import formatDateTimeToUTC

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
    data = request.get_json()
    return DarPlanEntrenamiento(data).execute()

@entrenamientos_blueprint.route('/plan-entrenamiento/crear', methods=['POST'])
def crear_plan_entrenamiento():
    data = request.get_json()
    headers = request.headers
    plan_entrenamiento = CrearPlanEntrenamiento(data, headers).execute()
    return  jsonify(plan_entrenamiento)