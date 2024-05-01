# Importación de dependencias
import traceback
from commands.base_command import BaseCommannd
from validators.validators import validar_emergency_contacts, validar_esquema, notificacion_alerta_esquema, validar_headers, validar_permisos_usuario
from sqlalchemy.exc import SQLAlchemyError
from utilities.utilities import consumir_servicio_usuarios, obtener_tipo_notificacion, publicar_pub_sub
from errors.errors import ApiError
from flask.json import jsonify

# Clase que contiene la logica de creción de Alerta
class CrearAlerta(BaseCommannd):
    def __init__(self, data, headers):
        validar_headers(headers)
        self.headers = headers
        self.validar_request(data)
        self.asignar_datos(data)

    # Función que valida el request del servicio
    def validar_request(self, request_json):
        # Validacion del request
        validar_esquema(request_json, notificacion_alerta_esquema)

    # Función que valida el request del servicio
    def asignar_datos(self, data):
        # Asignacion de variables
        self.latitud = data['latitud']
        self.longitud = data['longitud']
        self.descripcion = data['descripcion']

    # Función que realiza creación de la Alerta
    def execute(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            validar_emergency_contacts(response)
            alerta_msg = {
                "tipo": obtener_tipo_notificacion(),
                "emails": response['contactos_emergencia'],
                "usuario":  f"{response['nombres']} {response['apellidos']}",
                "latitud": self.latitud,
                "longitud": self.longitud,
                "descripcion": self.descripcion,
            }
            publicar_pub_sub(alerta_msg)
            return alerta_msg, 200  
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)        