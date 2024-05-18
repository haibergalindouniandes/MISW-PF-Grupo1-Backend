# Importación de dependencias
import os
from commands.base_command import BaseCommannd
from validators.validators import validar_esquema, notificacion_esquema, validar_headers, validar_permisos_usuario
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, SchedulingResultsNotFound
from models.models import AgendaServicios, db, Notificaciones
from flask.json import jsonify
from utilities.utilities import consumir_servicio_usuarios, obtener_tipo_notificacion, publicar_pub_sub


import traceback

# Clase que contiene la logica de creción de Notificaicon Masiva
class CrearNotificaiconMasiva(BaseCommannd): # pragma: no cover
    def __init__(self, data, headers):
        validar_headers(headers)
        self.headers = headers
        self.validar_request(data)
        self.asignar_datos(data)

    # Función que valida el request del servicio
    def validar_request(self, notificacion_json):
        # Validacion del request
        validar_esquema(notificacion_json, notificacion_esquema)        

    # Función que valida el request del servicio
    def asignar_datos(self, json_payload):
        # Asignacion de variables
        self.id_servicio = json_payload['id_servicio']
        self.descripcion = json_payload['descripcion']

    # Función que obtiene un array con los emails de los usuarios que agendaron un servicio
    def obtener_emails_agendamiento(self, data):
        # Obtener emails agendamiento
        return [agendamiento.email for agendamiento in data]
        
    # Función que consulta los emails de los usuarios que agendaron
    def consultar_emails_agendamiento(self, id_servicio):
        # Consultar por id_servicio
        agendamientos = db.session.query(AgendaServicios).filter_by(id_servicio = id_servicio).all()        
        if len(agendamientos) == 0:
            raise SchedulingResultsNotFound
        return self.obtener_emails_agendamiento(agendamientos)
    
    # Función que realiza creación de la Notificacion Masiva
    def execute(self):
        try:
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            notificacion_msg = {
                "tipo": obtener_tipo_notificacion(),
                "emails": self.consultar_emails_agendamiento(self.id_servicio),
                "usuario":  f"{response['nombres']} {response['apellidos']}",
                "descripcion": self.descripcion,
            }
            publicar_pub_sub(notificacion_msg)
            return notificacion_msg, 200   
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
    def registrar_notificacion(self):
            # Registrar en BD
            notifcacion = Notificaciones(
                name=self.name,
                latitud=self.latitud,
                longitud=self.longitud,
                descripcion=self.descripcion,
                tipo=self.tipo
            )
            db.session.add(notifcacion)
            #db.session.commit()
            return notifcacion