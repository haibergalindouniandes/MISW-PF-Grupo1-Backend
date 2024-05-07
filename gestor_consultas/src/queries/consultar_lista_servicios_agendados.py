import traceback
from queries.consultar_usuario import ConsultarUsuario
from validators.validators import validar_permisos_usuario
from queries.base_query import BaseQuery
from models.models import AgendaServicios, Usuario, db, Servicios, ConsultaServiciosAgendadosSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, BadRequest, TokenNotFound, NoRecordsFound
from datetime import datetime
from sqlalchemy import func, String

# Esquemas
consulta_servicios_schema = ConsultaServiciosAgendadosSchema()

# Clase que contiene la logica de consulta de todos los servicios agendados por usuario
class ConsultarListaServiciosAgendados(BaseQuery):
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
    
    # Función que realiza la consulta de la lista de servicios agendados
    def query(self):
        try:
            # Logica de negocio
            response = ConsultarUsuario(self.headers).query()
            validar_permisos_usuario(response)
            query = db.session.query(
                Servicios.id,
                Servicios.lugar,
                Servicios.nombre,
                Servicios.costo,
                AgendaServicios.fecha,
                AgendaServicios.hora,
                Servicios.descripcion,
                func.concat(Usuario.nombres, ' ', Usuario.apellidos).label('nombre_proveedor')
            ).join(
                AgendaServicios, AgendaServicios.id_servicio == func.cast(Servicios.id, String)
            ).join(
                Usuario, func.cast(Usuario.id, String) == func.cast(Servicios.id_usuario, String)
            ).filter(
                Servicios.fecha > datetime.now(),
                AgendaServicios.id_usuario == response['id']
            ).order_by(
                Servicios.fecha.asc()
            )
            servicios = query.all()
            if not servicios:
                raise NoRecordsFound
            return [consulta_servicios_schema.dump(servicio) for servicio in servicios]
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            db.session.rollback()
            raise ApiError(e)
        
