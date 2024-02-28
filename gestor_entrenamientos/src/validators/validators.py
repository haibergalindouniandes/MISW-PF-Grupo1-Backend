# Importación de dependencias
from errors.errors import BadRequest
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

# Función que valida los Schemad de las peticiones
def validateSchema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest