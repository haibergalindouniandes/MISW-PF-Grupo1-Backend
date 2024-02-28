# Importación de dependencias
from commands.base_command import BaseCommannd
from validators.validators import validateSchema, notificacionSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError
from flask.json import jsonify

import traceback

# Clase que contiene la logica de creción de Notificaicon Masiva
class CrearNotificaiconMasiva(BaseCommannd):
    def __init__(self, data):
        self.validateRequest(data)

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
            #TODO: Consulta de Emails de usuarios a Gestor de Consultas
            #TODO: Encolar peticion a Pub/Sub
            return jsonify({'msg': 'Notificacion Masiva enviada a cola de mensajes'}), 200  
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)