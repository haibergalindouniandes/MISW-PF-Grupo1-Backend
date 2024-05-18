import re
import traceback
from validators.validators import validar_permisos_usuario
from utilities.utilities import consumir_servicio_usuarios
from queries.base_query import BaseQuery
from models.models import db, Alimentacion, PlanAlimentacion, AlimentacionSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, BadRequest, TokenNotFound, FeedingResultsNotFound

# Esquemas
alimentacion_schema = AlimentacionSchema()

# Clase que contiene la logica de consulta de usuarios
class ConsultarPlanAlimentacionPorUsuario(BaseQuery):
    id_usuario: str
    # Constructor
    def __init__(self, id_usuario, headers):
        self.validar_request(id_usuario)
        self.validar_headers(headers)
        
    # Función que valida los headers del servicio
    def validar_headers(self, headers):
        # Validacion si existe el header Authorization
        if 'Authorization' in headers:
            auth_header = headers['Authorization']
            # Verificar si el encabezado Authorization comienza con "Bearer"
            if not auth_header.startswith('Bearer '):
                raise BadRequest
            self.headers = headers
        else:
            raise TokenNotFound

    # Función que valida el request del servicio
    def validar_request(self, id_usuario):
        if id_usuario == None:
            raise BadRequest
        self.id_usuario = id_usuario
    
    
    # Función que realiza de consulta del plan de alimentacion con base al id_usuario
    def query(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            alimentacion =  Alimentacion.query.filter_by(id_usuario=self.id_usuario).first()
            if alimentacion == None:
                raise FeedingResultsNotFound
            return alimentacion_schema.dump(alimentacion)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
