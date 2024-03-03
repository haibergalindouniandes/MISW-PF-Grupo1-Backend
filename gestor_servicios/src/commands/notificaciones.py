# Importación de dependencias
import os
from commands.base_command import BaseCommannd
from validators.validators import validateSchema, notificacionSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError
from models.models import db, Notificaciones
from flask.json import jsonify
from utilities.utilities import publicar_pub_sub


import traceback

# Clase que contiene la logica de creción de Notificaicon Masiva
class CrearNotificaiconMasiva(BaseCommannd):
    def __init__(self, data):
        self.validateRequest(data)
        #TODO: Email de prueba para el experimento
        self.emails = ["shiomarsa_2@hotmail.com",
                     "jf.guzmanc1@uniandes.edu.co"] 

    # Función que valida el request del servicio
    def validateRequest(self, notificacionJSON):
        # Validacion del request
        validateSchema(notificacionJSON, notificacionSchema)
        # Asignacion de variables
        self.id_trigger = notificacionJSON['id_trigger']
        self.latitud = notificacionJSON['latitud']
        self.longitud = notificacionJSON['longitud']
        self.descripcion = notificacionJSON['descripcion']

    # Función que realiza creación de la Notificacion Masiva
    def execute(self):
        try:
            #TODO: Consulta de Emails de usuarios a Gestor de Consultasc
            #TODO: Consulta de Nombre del Servicio a Gestor de Consultas
            for email in self.emails:
                notificaciones_msg = {
                   "tipo": "Noti_Masiva",
                    "email": email,
                    "name":  self.id_trigger,
                    "descripcion": self.descripcion,
                }
                publicar_pub_sub(notificaciones_msg)
            return jsonify({'msg': 'Notificacion Masiva enviada a cola de mensajes'}), 200  
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