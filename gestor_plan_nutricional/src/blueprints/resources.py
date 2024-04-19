from flask import request, Blueprint
from flask.json import jsonify
from commands.registrar_resultados_alimentacion import RegistrarResultadosAlimentacion
from commands.crear_plan_alimentacion import CrearPlanAlimentacion
from queries.resultados_alimenticios_por_usuario import ConsultarResultadosAlimentacionPorUsuario
from queries.resultados_alimenticios_por_fechas import ConsultarResultadosAlimentacionPorUsuarioFechas

planes_nutricionales_blueprint = Blueprint(name='nutricion', import_name=__name__, url_prefix='/nutricion')

# Recurso que expone la funcionalidad healthcheck
@planes_nutricionales_blueprint.route('/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone la funcionalidad de registro de los resultados de alimentacion
@planes_nutricionales_blueprint.route('/resultados-alimentacion', methods=['POST'])
def registrar_resultados_alimentacion():
    headers = request.headers
    data = request.get_json()
    resultados_alimentacion = RegistrarResultadosAlimentacion(data, headers).execute()
    return jsonify(resultados_alimentacion)

# Recurso que expone la funcionalidad de consulta de los resultados de alimentacion de un usuario por rango de fechas
@planes_nutricionales_blueprint.route('/resultados-alimentacion/<id_usuario>/<fecha_inicio>/<fecha_fin>', methods=['GET'])
def consultar_resultados_alimentacion_por_fechas(id_usuario, fecha_inicio, fecha_fin):
    headers = request.headers
    resultados_alimentacion = ConsultarResultadosAlimentacionPorUsuarioFechas(id_usuario, fecha_inicio, fecha_fin, headers).query()
    return jsonify(resultados_alimentacion)

# Recurso que expone la funcionalidad de consulta de los resultados de alimentacion de un usuario
@planes_nutricionales_blueprint.route('/resultados-alimentacion/<id_usuario>', methods=['GET'])
def consultar_resultados_alimentacion_por_usuario(id_usuario):
    headers = request.headers
    resultados_alimentacion = ConsultarResultadosAlimentacionPorUsuario(id_usuario, headers).query()
    return jsonify(resultados_alimentacion)

# Recurso que expone la creación de plan de entrenamiento
@planes_nutricionales_blueprint.route('/plan-nutricional', methods=['POST'])
def crear_plan_alimentacion():
    data = request.get_json()
    headers = request.headers
    plan_alimentacion = CrearPlanAlimentacion(data, headers).execute()
    return  jsonify(plan_alimentacion)