from flask import request, Blueprint
from commands.registrar_usuario import RegistrarUsuario
from queries.consultar_usuario import ConsultarUsuario
from utilities.utilities import generar_token
from queries.iniciar_sesion import IniciarSesion

usuarios_blueprint = Blueprint('usuarios', __name__)

# Recurso que expone la funcionalidad healthcheck
@usuarios_blueprint.route('/usuarios/ping', methods=['GET'])
def health():
    return "pong"

# Recurso que expone la funcionalidad registro de usuarios
@usuarios_blueprint.route('/usuarios', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    return RegistrarUsuario(data).execute()

# Recurso que expone la funcionalidad login de usuarios
@usuarios_blueprint.route('/usuarios/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    usuario = IniciarSesion(data).query()
    token_de_acceso = generar_token(usuario)
    return {"token": token_de_acceso, "id": usuario.id, "nombres": usuario.nombres, "tipo_usuario":usuario.tipo_usuario,"tipo_plan":usuario.tipo_plan}

# Recurso que expone la funcionalidad login de usuarios
@usuarios_blueprint.route('/usuarios/me', methods=['GET'])
def consulta_usuario():
    headers = request.headers
    usuario = ConsultarUsuario(headers).query()
    return usuario.to_dict()