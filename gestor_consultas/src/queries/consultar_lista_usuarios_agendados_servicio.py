import traceback
from queries.consultar_usuario import ConsultarUsuario
from validators.validators import validar_permisos_proveedor
from queries.base_query import BaseQuery
from models.models import AgendaServicios, Usuario, db, ConsultaUsuariosAgendadosServicioSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, BadRequest, TokenNotFound, NoRecordsFound
from sqlalchemy import func, String

# Esquemas
consulta_usuarios_agendamiento = ConsultaUsuariosAgendadosServicioSchema()

# Clase que contiene la logica de consulta de todos los servicios agendados por usuario
class ConsultarListaUsuariosAgendadosPorServicio(BaseQuery):
    # Constructor
    def __init__(self, id_servicio, headers):        
        self.validar_id_servicio(id_servicio)
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

    # Función que valida el id_servicio del servicio
    def validar_id_servicio(self, id_servicio):
        # Validacion si el id_servicio no viene vacio
        if not id_servicio or len(id_servicio) != 36:
            raise BadRequest
        self.id_servicio = id_servicio
    
    # Función que realiza la consulta de la lista de servicios agendados
    def query(self):
        try:
            # Logica de negocio
            response = ConsultarUsuario(self.headers).query()
            validar_permisos_proveedor(response)
            query = db.session.query(
                AgendaServicios.id_usuario,
                func.concat(Usuario.nombres, ' ', Usuario.apellidos).label('nombre_usuario'),
                AgendaServicios.email,
                AgendaServicios.fecha,
                AgendaServicios.hora,
                Usuario.pais_residencia,
                Usuario.ciudad_residencia
            ).join(
                Usuario, func.cast(Usuario.id, String) == func.cast(AgendaServicios.id_usuario, String)
            ).filter(
                func.cast(AgendaServicios.id_servicio, String) == self.id_servicio
            ).order_by(
                Usuario.nombres.desc()
            )
            usuarios_agendados = query.all()
            if not usuarios_agendados:
                raise NoRecordsFound
            return [consulta_usuarios_agendamiento.dump(usuario) for usuario in usuarios_agendados]
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
