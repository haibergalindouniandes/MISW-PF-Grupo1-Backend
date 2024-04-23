from flask import request, Blueprint
from flask.json import jsonify
from queries.consultar_por_usuario import ConsultarPlanAlimentacionPorUsuario
import json

consultas_blueprint = Blueprint(name='consultas', import_name=__name__, url_prefix='/consultas')

# Recurso que expone la funcionalidad healthcheck
@consultas_blueprint.route('/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone consulta de plan de entrenamiento con base al id_usuario
@consultas_blueprint.route('/plan-alimentacion/usuario/<id_usuario>', methods=['GET'])
def consultar_plan_alimentacion_por_usuario(id_usuario):
    headers = request.headers
    plan_entrenamiento = ConsultarPlanAlimentacionPorUsuario(id_usuario, headers).query()    
    return jsonify(plan_entrenamiento)

