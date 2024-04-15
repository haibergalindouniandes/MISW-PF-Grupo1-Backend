# Importación de dependencias
import traceback
from commands.base_command import BaseCommannd
from validators.validators import validar_permisos_usuario, validar_esquema, resultados_alimentacion_esquema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, BadRequest, TokenNotFound
from models.models import db, ResultadosAlimentacion, ResultadosAlimentacionSchema
from utilities.utilities import consumir_servicio_usuarios

# Esquemas
resultados_alimentacion_schema = ResultadosAlimentacionSchema()

# Clase que contiene la logica de registro de los resultados de alimentacion       
class RegistrarResultadosAlimentacion(BaseCommannd):
    # Constructor
    def __init__(self, data, headers):
        self.validar_headers(headers)        
        self.validateRequest(data)
        self.asignar_datos(data)

    # Función que valida el request del servicio
    def validateRequest(self, request_json):
        validar_esquema(request_json, resultados_alimentacion_esquema)

    # Función que valida los headers del servicio
    def validar_headers(self, headers):
        if 'Authorization' in headers:
            auth_header = headers['Authorization']
            if not auth_header.startswith('Bearer '):
                raise BadRequest
            self.headers = headers
        else:
            raise TokenNotFound

    # Función que valida el request del servicio
    def asignar_datos(self, json_payload):
        # Asignacion de variables
        self.calorias_1 = json_payload['calorias_1']
        self.calorias_2 = json_payload['calorias_2']
        self.calorias_3 = json_payload['calorias_3']
        self.ml_agua = json_payload['ml_agua']
        self.fecha = json_payload['fecha']
        self.id_usuario = json_payload['id_usuario']
       

   # Función que realiza el registro en BD
    def registrar_resultados_alimentacion_bd(self):
        # Validar y eliminar si existe un resultado de alimentacion con el id_usaurio y la fecha
        resultados_alimentacion = ResultadosAlimentacion.query.filter_by(id_usuario=self.id_usuario, fecha = self.fecha).first()
        if resultados_alimentacion:
            db.session.delete(resultados_alimentacion)
            db.session.commit()
        
        # Registrar en BD
        nuevo_resultados_alimentacion = ResultadosAlimentacion(
            calorias_1=self.calorias_1,
            calorias_2=self.calorias_2,
            calorias_3=self.calorias_3,
            ml_agua=self.ml_agua,
            fecha=self.fecha,
            id_usuario=self.id_usuario
        )
        
        db.session.add(nuevo_resultados_alimentacion)
        db.session.commit()
        return nuevo_resultados_alimentacion

    # Función que 
    def execute(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            resultados_alimentacion = self.registrar_resultados_alimentacion_bd()            
            return resultados_alimentacion_schema.dump(resultados_alimentacion)
        except IntegrityError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)
        except SQLAlchemyError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)