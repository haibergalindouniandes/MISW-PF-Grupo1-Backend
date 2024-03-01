# Importación de dependencias
import traceback
from src.commands.base_command import BaseCommannd
from src.validators.validators import validateSchema, planEntrenamientoEsquema
from sqlalchemy.exc import SQLAlchemyError
from src.errors.errors import ApiError
from flask.json import jsonify


# Clase que contiene la logica de creción de Alerta
class DarPlanEntrenamiento(BaseCommannd):
    def __init__(self, data):
        self.validateRequest(data)

    # Función que valida el request del servicio
    def validateRequest(self, request_json):
        # Validacion del request
        validateSchema(request_json, planEntrenamientoEsquema)
        # Asignacion de variables
        self.sexo = request_json["sexo"]
        self.peso = request_json["peso"]
        self.estatura = request_json["estatura"]
        self.enfermedades_cardiovasculares = request_json["enfermedades_cardiovasculares"]
        self.practica_deporte = request_json["practica_deporte"]
        self.proposito = request_json["proposito"]

    # Función que realiza creación de la Alerta
    def execute(self):
        try:
            pass           
            
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        

        