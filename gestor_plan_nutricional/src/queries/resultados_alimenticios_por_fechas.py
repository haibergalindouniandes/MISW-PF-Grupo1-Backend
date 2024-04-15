import re
import traceback
from validators.validators import validar_formato_fecha, validar_permisos_usuario
from utilities.utilities import consumir_servicio_usuarios
from queries.base_query import BaseQuery
from models.models import db, ResultadosAlimentacion, ResultadosAlimentacionSchema
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, BadRequest, TokenNotFound, FeedingResultsNotFound

# Esquemas
resultados_alimentacion_schema = ResultadosAlimentacionSchema()

# Clase que contiene la logica de consulta de usuarios
class ConsultarResultadosAlimentacionPorUsuarioFechas(BaseQuery):
    # Constructor
    def __init__(self, id_usuario, fecha_inicio, fecha_fin, headers):
        self.validar_request(id_usuario, fecha_inicio, fecha_fin)
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
    def validar_request(self, id_usuario, fecha_inicio, fecha_fin):
        if id_usuario == None:
            raise BadRequest
        self.id_usuario = id_usuario
        self.validar_fechas(fecha_inicio, fecha_fin)

    # Función que valida las fechas
    def validar_fechas(self, fecha_inicio, fecha_fin):
        validar_formato_fecha(fecha_inicio)
        validar_formato_fecha(fecha_fin)
        self.fecha_inicio = fecha_inicio
        self.fecha_fin= fecha_fin
    
    # Función que realiza de consulta de los resultados de alimentacion con base al id_usuario y un rango de fechas
    def query(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            resultados_alimentacion = db.session.query(ResultadosAlimentacion).filter_by(id_usuario = self.id_usuario).filter(ResultadosAlimentacion.fecha.between(self.fecha_inicio, self.fecha_fin)).order_by(ResultadosAlimentacion.fecha.desc()).all()
            if len(resultados_alimentacion) == 0:
                raise FeedingResultsNotFound
            return [resultados_alimentacion_schema.dump(resultado_alimentacion) for resultado_alimentacion in resultados_alimentacion]
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
