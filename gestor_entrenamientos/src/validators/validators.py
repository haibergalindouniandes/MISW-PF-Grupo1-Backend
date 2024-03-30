# Importación de dependencias
from errors.errors import BadRequest, CallExternalServiceError, Forbidden
from jsonschema import validate
import traceback
import jsonschema

# Esquemas
# Esquema para las alertas
alertaSchema = {
    "type": "object",
    "properties": {
        "id_trigger": {"type": "string", "minimum": 4, "maximum": 64},
        "latitud": {"type": "string", "minimum": 6, "maximum": 64},
        "longitud": {"type": "string", "minimum": 6, "maximum": 64},
        "descripcion":  {"type": "string", "minimum": 3, "maximum": 64},
    },
    "required": ["id_trigger", "latitud", "longitud", "descripcion"]
}

planEntrenamientoEsquema = {
    "type": "object",
    "properties": {
        "sexo": {"type": "string", "enum" : ["MASCULINO", "FEMENINO"]},
        "peso": {"type": "integer", "minimum": 40, "maximum": 200},  #kilogramos
        "estatura": {"type": "integer", "minimum": 140, "maximum": 200},  #centimetros
        "edad": {"type": "integer", "minimum": 18, "maximum": 90},
        "enfermedades_cardiovasculares": {"type": "string", "enum" : ["SI", "NO"]},
        "practica_deporte": {"type": "string", "enum" : ["SI", "NO"]},
        "proposito": {"type": "string", "enum" : ["GANAR MASA MUSCULAR", "PERDER PESO"]}
    },
    "required": ["sexo", "peso", "estatura", "edad", "enfermedades_cardiovasculares", "practica_deporte", "proposito"]
}

crearPlanEntrenamientoEsquema = {
    "type": "object",
    "properties": {
        "entrenamiento": {"type": "string"},
        "numero_semanas": {"type": "integer", "minimum": 1},
        "id_usuario": {"type": "string", "format": "uuid"},
        "plan_entrenamiento": {
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
    "required": ["entrenamiento", "numero_semanas", "id_usuario", "plan_entrenamiento"]
}

# Función que valida el http-response-code del consumo de un servicio
def validar_resultado_consumo_servicio(response):
    if response.status_code != 200:
        traceback.print_exc()
        raise CallExternalServiceError

# Función que valida el http-response-code del consumo de un servicio
def validar_permisos_usuario(response_json):
    if response_json['rol'] != 'PRO':
        raise Forbidden

# Función que valida los esquemas de las peticiones
def validateSchema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest