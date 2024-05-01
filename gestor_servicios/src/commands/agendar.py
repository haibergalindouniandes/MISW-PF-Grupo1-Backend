# Importación de dependencias
import os
from commands.base_command import BaseCommannd
from utilities.utilities import consumir_servicio_usuarios
from validators.validators import validar_esquema, esquema_agendar_servicio, validar_permisos_agendar_usuario
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, BadRequest, ServiceAlreadyRegistered, TokenNotFound
from models.models import db, AgendaServicios
import traceback

# Clase que contiene la logica del registro de un servicio
class AgendarServicio(BaseCommannd):
    # Constructor
    def __init__(self, data, headers):
        self.validar_headers(headers)
        self.validar_request(data)
        self.asignar_datos_agenda_servicio(data)

    # Función que valida el request del servicio
    def validar_request(self, json_payload):
        # Validacion del request
        validar_esquema(json_payload, esquema_agendar_servicio)
        
    # Función que valida los headers del servicio
    def validar_headers(self, headers):
        # Validacion si existe el header Authorization
        if 'Authorization' in headers:
            auth_header = headers['Authorization']
            # Verificar si el encabezado Authorization comienza con "Bearer"
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]  # Obtener el token Bearer
                self.token = token
                self.headers = headers
            else:
                raise BadRequest
        else:
            raise TokenNotFound

    # Función que valida el request del servicio
    def asignar_datos_agenda_servicio(self, json_payload):
        # Asignacion de variables
        self.id_usuario = json_payload['id_usuario']
        self.id_servicio = json_payload['id_servicio']
        self.email = json_payload['email']
        self.fecha = json_payload['fecha']
        self.hora = json_payload['hora']
        #self.descripcion = json_payload['descripcion']
        #self.lugar = json_payload['lugar']
        
        
    # Función que realiza el registro del usuario en BD
    def agendar_servicio_bd(self):
        # Registrar en BD
        servicio = AgendaServicios(
            id_usuario=self.id_usuario, 
            id_servicio=self.id_servicio,  
            email=self.email,
            fecha=self.fecha,  
            hora=self.hora  
            #lugar=self.lugar,
            #descripcion=self.descripcion            
        )
        db.session.add(servicio)
        db.session.commit()
        return servicio

    # Función que realiza creación del servicio
    def execute(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_agendar_usuario(response)
            servicio_agendado = self.agendar_servicio_bd()
            return servicio_agendado.to_dict()
        except IntegrityError as e:# pragma: no cover
            print(e)
            db.session.rollback()
            raise ServiceAlreadyRegistered(e)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        