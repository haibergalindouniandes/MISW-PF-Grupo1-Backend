from flask import request, Blueprint
from commands.registrar_usuario import RegistrarUsuario
from commands.consultar_usuario import ConsultarUsuario
from flask_jwt_extended import jwt_required, create_access_token
import hashlib
from models.models import db, Usuario
from flask_jwt_extended import jwt_required
import logging

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
    logging.info("Inicio Login Usuario")
    data = request.get_json()
    logging.info(data)
    usuario = ConsultarUsuario(data).execute()
    logging.info(usuario)
    db.session.commit()
    token_de_acceso = create_access_token(identity=request.json["password"])
    return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id, "nombres": usuario.nombres, "rol":usuario.rol,"plan":usuario.plan}
