# Importación de dependencias
import traceback
from commands.base_command import BaseCommannd
from validators.validators import validar_permisos_usuario, validateSchema, planEntrenamientoEsquema, crearPlanEntrenamientoEsquema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, BadRequest, TokenNotFound
from models.models import db, Entrenamientos, PlanEntrenamiento, EntrenamientoSchema
from utilities import utilities

# Esquemas
entrenamiento_schema = EntrenamientoSchema()

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
        self.edad = request_json["edad"]
        self.enfermedades_cardiovasculares = request_json["enfermedades_cardiovasculares"]
        self.practica_deporte = request_json["practica_deporte"]
        self.proposito = request_json["proposito"]

    # Función que retorna la recomendación de entrenamiento
    def execute(self):
        try:
            utilities.dar_clasificacion(self.sexo, self.peso, self.estatura, self.edad, self.enfermedades_cardiovasculares, self.practica_deporte)           
            planes_entrenamiento = utilities.recomendacion_planes_entrenamiento()
            planes_entrenamiento_keys = list(planes_entrenamiento.keys())
            return planes_entrenamiento[planes_entrenamiento_keys[0]]
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
class CrearPlanEntrenamiento(BaseCommannd):
    def __init__(self, data, headers):
        self.validar_headers(headers)        
        self.validateRequest(data)
        self.asignar_datos(data)

    # Función que valida el request del servicio
    def validateRequest(self, request_json):
        # Validacion del request
        validateSchema(request_json, crearPlanEntrenamientoEsquema)

    # Función que valida los headers del servicio
    def validar_headers(self, headers):
        # Validacion si existe el header Authorization
        if 'Authorization' in headers:
            auth_header = headers['Authorization']
            # Verificar si el encabezado Authorization comienza con "Bearer"
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]  # Obtener el token Bearer
                self.token = token
            else:
                raise BadRequest
        else:
            raise TokenNotFound

    # Función que valida el request del servicio
    def asignar_datos(self, json_payload):
        # Asignacion de variables
        self.entrenamiento = json_payload['entrenamiento']
        self.numero_semanas = json_payload['numero_semanas']
        self.id_usuario = json_payload['id_usuario']
        plan_entrenamiento = json_payload['plan_entrenamiento']
        self.lunes = plan_entrenamiento['lunes']
        self.martes = plan_entrenamiento['martes']
        self.miercoles = plan_entrenamiento['miercoles']
        self.jueves = plan_entrenamiento['jueves']
        self.viernes = plan_entrenamiento['viernes']
        self.sabado = plan_entrenamiento['sabado']
        self.domingo = plan_entrenamiento['domingo']

   # Función que realiza el registro del usuario en BD
    def registrar_plan_entrenamiento_bd(self):
        # Registrar en BD
        entrenamiento = Entrenamientos(
            entrenamiento=self.entrenamiento, 
            numero_semanas=self.numero_semanas,
            id_usuario=self.id_usuario
        )
        plan_entrenamiento = PlanEntrenamiento(
            lunes=self.lunes,
            martes=self.martes,
            miercoles=self.miercoles,
            jueves=self.jueves,
            viernes=self.viernes,
            sabado=self.sabado,
            domingo=self.domingo
        )
        entrenamiento.plan_entrenamiento = plan_entrenamiento
        db.session.add(entrenamiento)
        db.session.commit()
        db.session.refresh(entrenamiento)
        return entrenamiento

    # Función que retorna la recomendación de entrenamiento
    def execute(self):
        try:
            # Logica de negocio
            data = {
                "email": "preba@gmail.com",
                "password": "preba1223***"
            }
            response = utilities.consumir_servicio_usuarios(data)
            validar_permisos_usuario(response)
            entrenamiento = self.registrar_plan_entrenamiento_bd()            
            return entrenamiento_schema.dump(entrenamiento)
        except IntegrityError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e) 
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)