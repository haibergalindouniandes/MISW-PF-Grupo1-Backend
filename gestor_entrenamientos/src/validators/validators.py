# Importación de dependencias
from errors.errors import BadRequest, EmergencyContactsNotFound, Forbidden, TokenNotFound, Unauthorized
from jsonschema import validate
import traceback
import jsonschema
import os
import re
from errors.errors import BadDates, BadTime, BadRequest, Forbidden, Unauthorized
from datetime import date, time

# Esquemas
# Esquema para las alertas
notificacion_alerta_esquema = {
    "type": "object",
    "properties": {
        "latitud": {"type": "string", "minimum": 6, "maximum": 64},
        "longitud": {"type": "string", "minimum": 6, "maximum": 64},
        "descripcion":  {"type": "string", "minimum": 3, "maximum": 64},
    },
    "required": ["latitud", "longitud", "descripcion"]
}

planEntrenamientoEsquema = {
    "type": "object",
    "properties": {
        "sexo": {"type": "string", "enum" : ["MASCULINO", "FEMENINO"]},
        "peso": {"type": "integer", "minimum": 40, "maximum": 200}, 
        "estatura": {"type": "integer", "minimum": 140, "maximum": 200},
        "edad": {"type": "integer", "minimum": 18, "maximum": 90},
        "enfermedades_cardiovasculares": {"type": "string", "enum" : ["SI", "NO"]},
        "practica_deporte": {"type": "string", "enum" : ["SI", "NO"]},
        "proposito": {"type": "string", "enum" : ["GANAR MASA MUSCULAR", "PERDER PESO"]}
    },
    "required": ["sexo", "peso", "estatura", "edad", "enfermedades_cardiovasculares", "practica_deporte", "proposito"]
}

crear_plan_entrenamiento_esquema = {
    "type": "object",
    "properties": {
        "entrenamiento": {"type": "string", "enum" : ["Atletismo", "Ciclismo", "Carreras"]},
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

resultados_entrenamiento_esquema = {
    "type": "object",
    "properties": {
        "actividad": {"type": "string", "enum" : ["Ciclismo", "Atletismo"]},
        "distancia": {"type": "number", "minimum": 0},
        "vo2max": {"type": "number", "minimum": 0, "maximum": 100},
        "ftp": {"type": "number", "minimum": 0, "maximum": 600},
        "tiempo": {"type": "string"},
        "retroalimentacion": {"type": "string", "minimum": 4, "maximum": 32},
        "fecha": {"type": "string", "format": "date"},
        "id_usuario": {"type": "string"}
    },
    "required": ["actividad", "distancia", "tiempo", "retroalimentacion", "fecha", "id_usuario"]
}

# Función que valida el http-response-code del consumo de un servicio
def validar_resultado_consumo_servicio(response):
    if response.status_code != 200:
        traceback.print_exc()
        raise Unauthorized

# Función que valida el http-response-code del consumo de un servicio
def validar_permisos_usuario(response_json):
    if response_json['tipo_usuario'].lower() != os.getenv('ROL_PERMITIDO').lower():
        raise Forbidden

# Función que valida el formato de fecha
def validar_formato_fecha(fecha):
    try:
        date.fromisoformat(fecha)
    except ValueError:
        raise BadDates

# Función que valida el formato de hora
def validar_formato_hora(tiempo):
    try:
        time.fromisoformat(tiempo)
    except ValueError:
        raise BadTime

# Función que valida el resultado del entrenamiento
def validar_resultado_entrenamiento(response_json):
    if response_json['actividad'] == 'Ciclismo':
        if 'ftp' not in response_json:
            raise BadRequest
    if response_json['actividad'] == 'Atletismo':
        if 'vo2max' not in response_json:        
            raise BadRequest

# Función que valida los headers del servicio
def validar_headers(headers):
    if 'Authorization' in headers:
        auth_header = headers['Authorization']
        if not auth_header.startswith('Bearer '):
            raise BadRequest        
    else:
        raise TokenNotFound

# Función que valida si el usuario tiene contactos de emergencia
def validar_emergency_contacts(request_json):
    # Validacion contactos de emergencia
    if 'contactos_emergencia' not in request_json or request_json['contactos_emergencia'] == None:
        raise EmergencyContactsNotFound

# Función que valida los esquemas de las peticiones
def validar_esquema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest