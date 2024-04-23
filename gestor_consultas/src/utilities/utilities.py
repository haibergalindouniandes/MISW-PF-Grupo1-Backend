import os
import json
import requests
import traceback
from errors.errors import CallExternalServiceError
from validators.validators import validar_resultado_consumo_servicio


# Función retorna el enpoint del servicio de usuarios
def obtener_endpoint_usuarios():
    return os.getenv('GESTORUSUARIOS_ADDRESS')

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