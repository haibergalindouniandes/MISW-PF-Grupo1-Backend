# Importación de dependencias
import os
import re
from jsonschema import validate
import traceback
import jsonschema
from errors.errors import BadDates, BadRequest, Forbidden, Unauthorized

resultados_alimentacion_esquema = {
    "type": "object",
    "properties": {
        "calorias_1": {"type": "string", "pattern": "^[0-9]+$"},
        "calorias_2": {"type": "string", "pattern": "^[0-9]+$"},
        "calorias_3": {"type": "string", "pattern": "^[0-9]+$"},
        "ml_agua": {"type": "string", "pattern": "^[0-9]+$"},
        "fecha": {"type": "string", "format": "date"},
        "id_usuario": {"type": "string"}
    },
    "required": ["calorias_1", "calorias_2", "calorias_3", "ml_agua", "fecha", "id_usuario"]
}



crear_plan_alimentacion_esquema = {
    "type": "object",
    "properties": {
        "id_usuario": {"type": "string", "format": "uuid"},
        "numero_semanas": {"type": "integer", "minimum": 1},
        
        "plan_alimentacion": {
            "type": "object",
            "properties": {
                "lunes": {"type": "string", "pattern": "^[0-9]+$"},
                "martes": {"type": "string", "pattern": "^[0-9]+$"},
                "miercoles": {"type": "string", "pattern": "^[0-9]+$"},
                "jueves": {"type": "string", "pattern": "^[0-9]+$"},
                "viernes": {"type": "string", "pattern": "^[0-9]+$"},
                "sabado": {"type": "string", "pattern": "^[0-9]+$"},
                "domingo": {"type": "string", "pattern": "^[0-9]+$"}
            },
            "required": ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        }
    },
    "required": ["id_usuario", "numero_semanas",  "plan_alimentacion"]
}

# Función que valida el http-response-code del consumo de un servicio
def validar_resultado_consumo_servicio(response):
    if response.status_code != 200:
        traceback.print_exc()
        raise Unauthorized

# Función que valida el http-response-code del consumo de un servicio
def validar_permisos_usuario(response_json):
    if response_json['tipo_usuario'] != os.getenv('ROL_PERMITIDO'):
        raise Forbidden

# Función que valida el formato de fecha
def validar_formato_fecha(fecha):
    if not re.match(r'\d{4}-\d{2}-\d{2}', fecha):
        raise BadDates

# Función que valida los esquemas de las peticiones
def validar_esquema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest