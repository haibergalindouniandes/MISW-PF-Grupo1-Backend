# Importación de dependencias
import os
from commands.base_command import BaseCommannd
from utilities.utilities import consumir_servicio_usuarios
from validators.validators import validar_esquema, esquema_agendar_servicio, validar_headers, validar_permisos_agendar_usuario,validar_servicio_valido
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, BadRequest, ServiceAlreadyRegistered, TokenNotFound
from models.models import db, AgendaServicios,Servicios
import traceback

# Clase que contiene la logica del registro de un servicio
class AgendarServicio(BaseCommannd):
    # Constructor
    def __init__(self, data, headers):
        validar_headers(headers)
        self.headers = headers
        self.validar_request(data)
        self.asignar_datos_agenda_servicio(data)

    # Función que valida el request del servicio
    def validar_request(self, json_payload):
        # Validacion del request
        validar_esquema(json_payload, esquema_agendar_servicio)

    def validar_servicio(self):
        # Validacion del id_servicio
        servicio = Servicios.query.filter_by(id_servicio=self.id_servicio).first()
        validar_servicio_valido(servicio, self.fecha)
        
        
    # Función que valida el request del servicio
    def asignar_datos_agenda_servicio(self, json_payload):
        # Asignacion de variables
        self.id_usuario = json_payload['id_usuario']
        self.id_servicio = json_payload['id_servicio']
        self.email = json_payload['email']
        self.fecha = json_payload['fecha']
        self.hora = json_payload['hora']
        
    # Función que realiza el registro del usuario en BD
    def agendar_servicio_bd(self):
        # Validar y eliminar si existe un plan de entrenamiento con el id_usaurio
        agenda_usuario = AgendaServicios.query.filter_by(id_usuario=self.id_usuario, id_servicio=self.id_servicio).first()
        if agenda_usuario:
            db.session.add(agenda_usuario)
            db.session.commit()
            return agenda_usuario
        else:
            # Registrar en BD
            servicio = AgendaServicios(
                id_usuario=self.id_usuario, 
                id_servicio=self.id_servicio,  
                email=self.email,
                fecha=self.fecha,  
                hora=self.hora        
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
        