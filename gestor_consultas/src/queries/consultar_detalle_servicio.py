import traceback
from validators.validators import validar_permisos_usuario
from utilities.utilities import consumir_servicio_usuarios
from queries.base_query import BaseQuery
from models.models import db, Servicios, ConsultaDetalleServicioSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, BadRequest, TokenNotFound, NoRecordsFound
from datetime import datetime


consulta_detalle_servicio_schema = ConsultaDetalleServicioSchema()

# Clase que contiene la logica de consulta del detalle del servicio
class ConsultarDetalleServicio(BaseQuery):
    # Constructor
    def __init__(self, id_servicio, headers):        
        self.validar_headers(headers)
        self.validate_request(id_servicio)
        
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
    def validate_request(self, id_servicio):
        if id_servicio == None:
            raise BadRequest
        self.id_servicio = id_servicio

    # Función que realiza la consulta del detalle del servicio con base al id_detalle
    def query(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            servicio = db.session.query(Servicios).filter((Servicios.id == self.id_servicio) & (Servicios.fecha > datetime.now())).first()
            if servicio == None:
                raise NoRecordsFound
            return consulta_detalle_servicio_schema.dump(servicio)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
