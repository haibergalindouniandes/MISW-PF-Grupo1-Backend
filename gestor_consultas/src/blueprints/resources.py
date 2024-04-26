from flask import request, Blueprint
from flask.json import jsonify
from src.queries.consultar_plan_alimentacion_por_usuario import ConsultarPlanAlimentacionPorUsuario
from src.queries.consultar_resultado_entrenamiento_por_usuario import ConsultarResultadoEntrenamientoPorUsuario
from src.queries.consultar_usuario import ConsultarUsuario


consultas_blueprint = Blueprint(name='consultas', import_name=__name__, url_prefix='/consultas')

# Recurso que expone la funcionalidad healthcheck
@consultas_blueprint.route('/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone consulta de plan de alimentacion con base al id_usuario
@consultas_blueprint.route('/plan-alimentacion/usuario/<id_usuario>', methods=['GET'])
def consultar_plan_alimentacion_por_usuario(id_usuario):
    headers = request.headers
    plan_alimentacion = ConsultarPlanAlimentacionPorUsuario(id_usuario, headers).query()    
    return jsonify(plan_alimentacion)

# Recurso que expone consulta de resultado de entrenamiento con base al id_usuario
@consultas_blueprint.route('/resultado-entrenamiento/usuario/<id_usuario>', methods=['GET'])
def consultar_resultado_entrenamiento_por_usuario(id_usuario):
    headers = request.headers
    resultado_entrenamiento = ConsultarResultadoEntrenamientoPorUsuario(id_usuario, headers).query()    
    return jsonify(resultado_entrenamiento)

# Recurso que expone consulta de usuarios
@consultas_blueprint.route('/usuarios/me', methods=['GET'])
def consultar_usuario():
    headers = request.headers
    resultado_consulta_usuario = ConsultarUsuario(headers).query()
    return jsonify(resultado_consulta_usuario)
