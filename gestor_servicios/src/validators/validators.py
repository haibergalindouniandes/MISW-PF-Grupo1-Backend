# Importación de dependencias
import os
import traceback
import jsonschema
from errors.errors import BadRequest, Forbidden, Unauthorized
from jsonschema import validate

# Esquemas
# Esquema para las alertas
notificacionSchema = {
    "type": "object",
    "properties": {
        "id_trigger": {"type": "string", "minimum": 4, "maximum": 64},
        "latitud": {"type": "string", "minimum": 6, "maximum": 64},
        "longitud": {"type": "string", "minimum": 6, "maximum": 64},
        "descripcion":  {"type": "string", "minimum": 3, "maximum": 64},
    },
    "required": ["id_trigger", "descripcion"]
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
        "fecha": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$"},
        "id_usuario": {"type": "string", "minLength": 1, "maxLength": 36}
    },
    "required": ["nombre", "descripcion", "frecuencia", "costo", "numero_minimo_participantes", "numero_maximo_participantes", "lugar", "fecha", "id_usuario"]
}

# Esquema para registrar un servicio
esquema_agendar_servicio = {
    "type": "object",
    "properties": {
        "id_usuario": {"type": "string", "minLength": 1, "maxLength": 36},
        "id_servicio": {"type": "string", "minLength": 1, "maxLength": 36},
        "email": {"type": "string", "minLength": 1, "maxLength": 200},
        "fecha": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$"},        
        "descripcion": {"type": "string", "minLength": 1, "maxLength": 1000},
        "lugar": {"type": "string", "minLength": 6, "maxLength": 200}                
    },
    "required": ["id_usuario", "id_servicio", "fecha", "descripcion", "lugar", "email"]
}

# Función que valida el http-response-code del consumo de un servicio
def validar_resultado_consumo_servicio(response):
    if response.status_code != 200:
        traceback.print_exc()
        raise Unauthorized

# Función que valida que un usuario tenga el rol necesario para consumir los servicios
def validar_permisos_usuario(response_json):
    if response_json['tipo_usuario'] == os.getenv('ROL_PERMITIDO'):
        raise Forbidden

# Función que valida los esquemas de las peticiones
def validar_esquema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest