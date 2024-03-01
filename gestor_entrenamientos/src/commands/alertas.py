# Importación de dependencias
import traceback
from src.commands.base_command import BaseCommannd
from src.validators.validators import validateSchema, alertaSchema
from sqlalchemy.exc import SQLAlchemyError
from src.utilities.utilities import publicar_pub_sub
from src.errors.errors import ApiError
from flask.json import jsonify


# Clase que contiene la logica de creción de Alerta
class CrearAlerta(BaseCommannd):
    def __init__(self, data):
        self.validateRequest(data)
        #TODO: Email de prueba para el experimento
        self.email = "s.salazarc@uniandes.edu.co"

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
            #TODO: Consulta de Nombre de Usuario contacto de emergencia a Gestor de Consultas
            alerta_msg = {
                "tipo": "Alerta",
                "email": self.email,
                "name":  self.id_trigger,
                "latitud": self.latitud,
                "longitud": self.longitud,
                "descripcion": self.descripcion,
            }
            publicar_pub_sub(alerta_msg)
            return jsonify({'msg': 'Alerta enviada a cola de mensajes'}), 200  
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        

        