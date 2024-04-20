# Importación de dependencias
import traceback
from commands.base_command import BaseCommannd
from validators.validators import validar_permisos_usuario, validar_resultado_entrenamiento, validar_esquema, validar_formato_fecha, validar_formato_hora, resultados_entrenamiento_esquema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, BadRequest, TokenNotFound
from models.models import db, ResultadosEntrenamiento, ResultadosEntrenamientoSchema
from utilities.utilities import consumir_servicio_usuarios
from datetime import date, time

# Esquemas
resultados_entrenamiento_schema = ResultadosEntrenamientoSchema()

# Clase que contiene la logica de registro de los resultados de entrenamiento       
class RegistrarResultadosEntrenamiento(BaseCommannd):
    # Constructor
    def __init__(self, data, headers):
        self.validar_headers(headers)        
        self.validateRequest(data)
        self.validar_resultados(data)
        self.asignar_datos(data)

    # Función que valida el request del servicio
    def validateRequest(self, request_json):
        validar_esquema(request_json, resultados_entrenamiento_esquema)
        validar_formato_fecha(request_json['fecha'])
        validar_formato_hora(request_json['tiempo'])

    # Función que valida el request del servicio
    def validar_resultados(self, request_json):
        validar_resultado_entrenamiento(request_json)

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
        self.actividad = json_payload['actividad']
        self.distancia = json_payload['distancia']
        if json_payload['actividad'] == 'Ciclismo':
            self.ftp = float(json_payload['ftp'])
            self.vo2max = None
        if json_payload['actividad'] == 'Atletismo':
            self.vo2max = float(json_payload['vo2max'])
            self.ftp = None            
        self.tiempo = time.fromisoformat(json_payload['tiempo'])
        self.retroalimentacion = json_payload['retroalimentacion']
        self.fecha = date.fromisoformat(json_payload['fecha'])
        self.id_usuario = json_payload['id_usuario']
       

   # Función que realiza el registro en BD
    def registrar_resultados_entrenamiento_bd(self):
        # Validar y eliminar si existe un resultado de entrenamiento con id_usaurio, actividad y fecha dadas
        resultados_entrenamiento = ResultadosEntrenamiento.query.filter_by(id_usuario=self.id_usuario, actividad = self.actividad, fecha = self.fecha).first()
        if resultados_entrenamiento:
            db.session.delete(resultados_entrenamiento)
            db.session.commit()
        
        # Registrar en BD
        nuevo_resultados_entrenamiento = ResultadosEntrenamiento(
            actividad = self.actividad,
            distancia = self.distancia
            vo2max = self.vo2max,
            ftp = self.ftp,
            tiempo = self.tiempo,
            retroalimentacion = self.retroalimentacion,
            fecha = self.fecha,
            id_usuario = self.id_usuario
        )
        
        db.session.add(nuevo_resultados_entrenamiento)
        db.session.commit()
        return nuevo_resultados_entrenamiento

    # Función que 
    def execute(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            resultados_entrenamiento = self.registrar_resultados_entrenamiento_bd()
            return resultados_entrenamiento_schema.dump(resultados_entrenamiento)
        except IntegrityError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)
        except SQLAlchemyError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)