import traceback
from validators.validators import validar_permisos_usuario
from utilities.utilities import consumir_servicio_usuarios
from queries.base_query import BaseQuery
from queries.consultar_usuario import ConsultarUsuario
from models.models import db, Servicios, AgendaServicios, ConsultaServiciosSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import exists, and_, func, String
from errors.errors import ApiError, BadRequest, TokenNotFound, NoRecordsFound
from datetime import datetime


consulta_servicios_schema = ConsultaServiciosSchema()

# Clase que contiene la logica de consulta de todos los servicios disponibles
class ConsultarListaServicios(BaseQuery):
    # Constructor
    def __init__(self, headers):        
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
    
    # Función que realiza la consulta de la lista de servicios vigentes
    def query(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            usuario = ConsultarUsuario(self.headers).query()
            servicios = db.session.query(Servicios.id, Servicios.nombre, Servicios.costo, Servicios.lugar) \
                                  .filter((Servicios.fecha > datetime.now()) & (Servicios.estado == 'ACT')) \
                                  .filter(~exists().where(and_(func.cast(Servicios.id, String) == func.cast(AgendaServicios.id_servicio, String), func.cast(AgendaServicios.id_usuario, String) == usuario['id']))).all()
            if servicios == None:
                raise NoRecordsFound
            return [consulta_servicios_schema.dump(servicio) for servicio in servicios]
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            db.session.rollback()
            raise ApiError(e)
        
