# Importación de dependencias
from errors.errors import BadRequest, Forbidden, Unauthorized
from jsonschema import validate
import traceback
import jsonschema
import os
from errors.errors import BadRequest, Forbidden, Unauthorized


# Función que valida el http-response-code del consumo de un servicio
def validar_resultado_consumo_servicio(response):
    if response.status_code != 200:
        traceback.print_exc()
        raise Unauthorized

# Función que valida el http-response-code del consumo de un servicio
def validar_permisos_usuario(response_json):
    if response_json['tipo_usuario'].lower() != os.getenv('ROL_PERMITIDO').lower():
        raise Forbidden

# Función que valida los esquemas de las peticiones
def validar_esquema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest