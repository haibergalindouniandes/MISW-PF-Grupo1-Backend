# Importación de dependencias
import os
import traceback
import jsonschema
from errors.errors import BadRequest, Forbidden, TokenNotFound, Unauthorized
from jsonschema import validate
import logging
from datetime import datetime

# Esquemas
# Esquema para las notificaciones masivas
notificacion_esquema = {
    "type": "object",
    "properties": {
        "id_servicio": {"type": "string", "minimum": 4, "maximum": 64},
        "descripcion":  {"type": "string", "minimum": 3, "maximum": 64}
    },
    "required": ["id_servicio", "descripcion"]
}

# Esquema para registrar un servicio
esquema_registro_servicio = {
    "type": "object",
    "properties": {
        "nombre": {"type": "string", "minLength": 8, "maxLength": 200},
        "descripcion": {"type": "string", "minLength": 10, "maxLength": 1000},
        "frecuencia": {"type": "string"},
        "costo": {"type": "string"},
        "numero_minimo_participantes": {"type": "number"},
        "numero_maximo_participantes": {"type": "number"},
        "lugar": {"type": "string", "minLength": 6, "maxLength": 200},
        "fecha": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
        "id_usuario": {"type": "string", "minLength": 1, "maxLength": 36}
    },
    "required": ["nombre", "descripcion", "frecuencia", "costo", "numero_minimo_participantes", "numero_maximo_participantes", "lugar", "fecha", "id_usuario"]
}

# Esquema para registrar un servicio
esquema_agendar_servicio = {
    "type": "object",
    "properties": {
        "id_usuario": {"type": "string", "minLength": 1, "maxLength": 60},
        "id_servicio": {"type": "string", "minLength": 1, "maxLength": 60},
        "email": {"type": "string", "minLength": 1, "maxLength": 200},
        "fecha": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},        
        "hora": {"type": "string", "pattern": "^\\d{2}:\\d{2}:\\d{2}$"},        
        #"descripcion": {"type": "string", "minLength": 1, "maxLength": 1000},
        #"lugar": {"type": "string", "minLength": 6, "maxLength": 200}                
    },
    "required": ["id_usuario", "id_servicio", "fecha", "email", "hora"]
}

# Función que valida el http-response-code del consumo de un servicio
def validar_resultado_consumo_servicio(response):
    if response.status_code != 200:
        traceback.print_exc()
        raise Unauthorized

# Función que valida que un usuario tenga el rol necesario para consumir los servicios
def validar_permisos_usuario(response_json):
    if response_json['tipo_usuario'] != os.getenv('ROL_PERMITIDO'):
        raise Forbidden

# Función que valida que un usuario tenga el rol necesario para consumir los servicios
def validar_permisos_agendar_usuario(response_json):
    print(response_json['tipo_usuario'])
    logging.info('Response Json')
    logging.info(response_json['tipo_usuario'])
    logging.info('Env')
    logging.info(os.getenv('ROL_AGENDAR_USUARIO'))
    if response_json['tipo_usuario'] != os.getenv('ROL_AGENDAR_USUARIO'):
        raise Forbidden

# Función que valida que un usuario tenga el rol necesario para consumir los servicios
def validar_servicio_valido(servicio, date):
    date_format = '%Y-%m-%d'
    print('validar_servicio_valido')
    print(servicio.fecha)
    logging.info(datetime.strptime( date,date_format))
    if servicio.fecha >= datetime.strptime(date,date_format) and servicio.estado != 'ACT':
        raise Forbidden


# Función que valida los headers del servicio
def validar_headers(headers):
    # Validacion si existe el header Authorization
    if 'Authorization' in headers:
        auth_header = headers['Authorization']
        # Verificar si el encabezado Authorization comienza con "Bearer"
        if not auth_header.startswith('Bearer '):
            raise BadRequest        
    else:
        raise TokenNotFound

# Función que valida los esquemas de las peticiones
def validar_esquema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest