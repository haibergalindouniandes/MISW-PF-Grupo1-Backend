import traceback
from queries.base_query import BaseQuery
from models.models import EntrenamientoSchema, PlanEntrenamiento, db
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, BadRequest, TokenNotFound, TrainingPlanNotFound
from models.models import Entrenamientos

# Esquemas
entrenamiento_schema = EntrenamientoSchema()

# Clase que contiene la logica de consulta de usuarios
class ConsultarPlanEntrenamientoPorUsuario(BaseQuery):
    # Constructor
    def __init__(self, id_usuario, headers):
        self.id_usuario = id_usuario
        self.validar_headers(headers)
        
    # Función que valida los headers del servicio
    def validar_headers(self, headers):
        # Validacion si existe el header Authorization
        if 'Authorization' in headers:
            auth_header = headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                self.token = token
            else:
                raise BadRequest
        else:
            raise TokenNotFound
    
    # Función que realiza de consulta de un plan de entrenamiento con base al id_usuario
    def query(self):
        try:
            # Logica de negocio
            plan_entrenamiento = db.session.query(Entrenamientos).filter_by(id_usuario = self.id_usuario).first()
            if plan_entrenamiento == None:
                raise TrainingPlanNotFound
            return entrenamiento_schema.dump(plan_entrenamiento)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
