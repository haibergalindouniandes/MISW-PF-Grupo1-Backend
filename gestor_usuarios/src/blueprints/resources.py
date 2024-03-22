from flask import request, Blueprint
from commands.registrar_usuario import RegistrarUsuario
from commands.consultar_usuario import ConsultarUsuario
from flask_jwt_extended import jwt_required, create_access_token
import hashlib

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
    contrasena_encriptada = hashlib.md5(request.json["password"].encode('utf-8')).hexdigest()
    usuario = ConsultarUsuario(data).execute()
    #db.session.commit()
    token_de_acceso = create_access_token(identity=usuario.id)
    return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id, "rol": usuario.rol}
