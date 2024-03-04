# Importación de dependencias
import json
import traceback
from commands.base_command import BaseCommannd
from validators.validators import validateSchema, planNutricionalEsquema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError
from models.models import PlanNutricional, PlanNutricionalSchema
from utilities import utilities


plan_nutricion_schema = PlanNutricionalSchema()
class DarPlanNutricional(BaseCommannd):
    def __init__(self, data):
        self.validateRequest(data)

    # Función que valida el request del servicio
    def validateRequest(self, request_json):
        # Validacion del request
        validateSchema(request_json, planNutricionalEsquema)
        # Asignacion de variables
        self.sexo = request_json["sexo"]
        self.peso = request_json["peso"]
        self.estatura = request_json["estatura"]
        self.edad = request_json["edad"]
        self.enfermedades_cardiovasculares = request_json["enfermedades_cardiovasculares"]
        self.practica_deporte = request_json["practica_deporte"]
        self.proposito = request_json["proposito"]

    # Función que realiza creación de la Alerta
    def execute(self):
        try:
            utilities.dar_clasificacion(self.sexo, self.peso, self.estatura, self.edad, self.enfermedades_cardiovasculares, self.practica_deporte)           
            planes_nutricionales = utilities.recomendacion_planes_nutricionales()
            return planes_nutricionales["plan nutricional 1"]
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        

        