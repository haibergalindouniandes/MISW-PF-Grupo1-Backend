import os
import json
import requests
import traceback
import datetime
import jwt
from errors.errors import CallExternalServiceError, ExpiredToken, InvalidToken
from validators.validators import validar_resultado_consumo_servicio


JWT_SECRET_KEY =  os.environ["JWT_SECRET_KEY"]
# Función retorna el enpoint del servicio de usuarios
def obtener_endpoint_usuarios():
    return os.getenv('GESTORUSUARIOS_ADDRESS')

def validar_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        exp = payload['exp']
        exp_datetime = datetime.datetime.utcfromtimestamp(exp)
        now = datetime.datetime.utcnow()
        if now > exp_datetime:
            raise ExpiredToken
        return payload
    except jwt.ExpiredSignatureError:
        raise ExpiredToken
    except jwt.InvalidTokenError:
        raise InvalidToken       

# Funcion que hace el consumo GET de gestor de usuarios
def consumir_servicio_usuarios(headers):
    try:
        headers_servicio_usuario = {
            "Authorization": headers['Authorization']
        }
        response = requests.get(url=obtener_endpoint_usuarios(), headers=headers_servicio_usuario)
        validar_resultado_consumo_servicio(response)
        return response.json()
    except requests.exceptions.HTTPError as e: # pragma: no cover
        traceback.print_exc()
        raise CallExternalServiceError      