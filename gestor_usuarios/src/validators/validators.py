# Importación de dependencias
from errors.errors import BadRequest, ErrorConsumoServicioExterno
from jsonschema import validate
import traceback
import jsonschema

# Esquemas
# Esquema para el reigstro de usuario
esquema_registro_usuario = {
    "type": "object",
    "properties": {
        "nombres": {"type": "string", "minimum": 4, "maximum": 64},
        "apellidos": {"type": "string", "minimum": 4, "maximum": 64},
        "tipo_identificacion": {"type": "string", "minimum": 4, "maximum": 30},
        "numero_identificacion": {"type": "string", "minimum": 6, "maximum": 12},
        "sexo": {"type": "string", "enum" : ["MASCULINO", "FEMENINO"]},
        "edad": {"type": "integer", "minimum": 18, "maximum": 90},
        "estatura": {"type": "integer", "minimum": 140, "maximum": 200}, 
        "peso": {"type": "number"},
        "enfermedades_cardiovasculares": {"type": "boolean"},
        "practica_deporte": {"type": "boolean"},
        "proposito": {"type": "string", "enum" : ["GANAR MASA MUSCULAR", "PERDER PESO"]},
        "pais": {"type": "string", "minimum": 4, "maximum": 64},
        "departamento": {"type": "string", "minimum": 4, "maximum": 64},
        "ciudad": {"type": "string", "minimum": 4, "maximum": 64},
        "email": {"type": "string", "minimum": 4, "maximum": 100},
        "password": {"type": "string", "minimum": 4, "maximum": 250}
    },
    "required": ["nombres", "apellidos", "tipo_identificacion", "numero_identificacion", "sexo", "edad", "estatura", "enfermedades_cardiovasculares", "practica_deporte", "proposito","pais", "departamento", "ciudad", "email","password"]
}

# Función que valida los esquemas de las peticiones
def validar_esquema(datos_json, esquema):
    try:
        validate(instance=datos_json, schema=esquema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest
    
# Función que valida el http-response-code del consumo de un servicio
def validar_resultado_consumo_servicio(resultado):
    print('<================ validar_resultado_consumo_servicio =====================>')
    print(f'Http-response-code [{resultado.status}]')
    if resultado.status != 200:
        traceback.print_exc()
        raise ErrorConsumoServicioExterno