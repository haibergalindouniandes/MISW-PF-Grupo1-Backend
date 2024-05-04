from flask import request, Blueprint
from flask.json import jsonify
from queries.consultar_lista_servicios_agendados import ConsultarListaServiciosAgendados
from queries.consultar_lista_servicios_por_usuario import ConsultarListaServiciosPorUsuario
from queries.consultar_plan_alimentacion_por_usuario import ConsultarPlanAlimentacionPorUsuario
from queries.consultar_resultado_entrenamiento_por_usuario import ConsultarResultadoEntrenamientoPorUsuario
from queries.consultar_usuario import ConsultarUsuario
from queries.consultar_lista_servicios import ConsultarListaServicios
from queries.consultar_detalle_servicio import ConsultarDetalleServicio


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

# Recurso que expone consulta de todos los servicios
@consultas_blueprint.route('/servicios', methods=['GET'])
def consultar_lista_servicios():
    headers = request.headers
    resultado_consulta_servicios = ConsultarListaServicios(headers).query()
    return jsonify(resultado_consulta_servicios)

# Recurso que expone consulta de los detalles de un servicio con base al id del servicio
@consultas_blueprint.route('/servicios/<id_servicio>', methods=['GET'])
def consultar_detalle_servicio(id_servicio):
    headers = request.headers
    resultado_detalle_servicio = ConsultarDetalleServicio(id_servicio, headers).query()
    return jsonify(resultado_detalle_servicio)

# Recurso que expone consulta de todos los servicios de un usuario
@consultas_blueprint.route('/servicios/usuario', methods=['GET'])
def consultar_lista_servicios_por_usuario():
    headers = request.headers
    resultado_consulta_servicios = ConsultarListaServiciosPorUsuario(headers).query()
    return jsonify(resultado_consulta_servicios)

# Recurso que expone consulta de todos los servicios agendados de un usuario
@consultas_blueprint.route('/servicios/agendados', methods=['GET'])
def consultar_lista_servicios_agendados():
    headers = request.headers
    resultado_consulta_servicios = ConsultarListaServiciosAgendados(headers).query()
    return jsonify(resultado_consulta_servicios)