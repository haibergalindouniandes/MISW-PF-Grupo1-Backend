# Importación de dependencias
from commands.base_command import BaseCommannd
from validators.validators import validateSchema, alertaSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError
from flask.json import jsonify

import traceback

# Clase que contiene la logica de creción de Alerta
class CrearAlerta(BaseCommannd):
    def __init__(self, data):
        self.validateRequest(data)

    # Función que valida el request del servicio
    def validateRequest(self, alertaJSON):
        # Validacion del request
        validateSchema(alertaJSON, alertaSchema)
        # Asignacion de variables
        self.id_trigger = alertaJSON['id_trigger']
        self.latitud = alertaJSON['latitud']
        self.longitud = alertaJSON['longitud']
        self.descripcion = alertaJSON['descripcion']

    # Función que realiza creación de la Alerta
    def execute(self):
        try:
            #TODO: Consulta de Email de contacto de emergencia a Gestor de Consultas
            #TODO: Encolar peticion a Pub/Sub
            return jsonify({'msg': 'Alerta enviada a cola de mensajes'}), 200  
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)