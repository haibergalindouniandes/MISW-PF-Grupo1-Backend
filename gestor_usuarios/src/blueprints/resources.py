from flask import request, Blueprint
from commands.registrar_usuario import RegistrarUsuario

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