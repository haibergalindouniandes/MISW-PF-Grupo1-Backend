# Importación de dependencias
import traceback
from commands.base_command import BaseCommannd
from validators.validators import validar_permisos_usuario, validar_esquema, crear_plan_alimentacion_esquema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, BadRequest, TokenNotFound
from models.models import db, Alimentacion, PlanAlimentacion, PlanAlimentacionSchema, AlimentacionSchema
from utilities.utilities import consumir_servicio_usuarios

# Esquemas
alimentacion_schema = AlimentacionSchema()

# Clase que contiene la logica de creción de un plan de entrenamiento       
class CrearPlanAlimentacion(BaseCommannd):
    def __init__(self, data, headers):
        self.validar_headers(headers)        
        self.validateRequest(data)
        self.asignar_datos(data)

    # Función que valida el request del servicio
    def validateRequest(self, request_json):
        # Validacion del request
        validar_esquema(request_json, crear_plan_alimentacion_esquema)

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
    def asignar_datos(self, json_payload):
        # Asignacion de variables    
        self.id_usuario = json_payload['id_usuario']    
        self.numero_semanas = json_payload['numero_semanas']
        
        plan_alimentacion = json_payload['plan_alimentacion']
        self.lunes = plan_alimentacion['lunes']
        self.martes = plan_alimentacion['martes']
        self.miercoles = plan_alimentacion['miercoles']
        self.jueves = plan_alimentacion['jueves']
        self.viernes = plan_alimentacion['viernes']
        self.sabado = plan_alimentacion['sabado']
        self.domingo = plan_alimentacion['domingo']

   # Función que realiza el registro del usuario en BD
    def registrar_plan_nutricional_bd(self):
        # Validar y eliminar si existe un plan de entrenamiento con el id_usaurio
        plan_nutricional = Alimentacion.query.filter_by(id_usuario=self.id_usuario).first()
        if plan_nutricional:
            db.session.delete(plan_nutricional)
            db.session.commit()
        
        # Registrar en BD

        plan_alimentacion = PlanAlimentacion(
            lunes=self.lunes,
            martes=self.martes,
            miercoles=self.miercoles,
            jueves=self.jueves,
            viernes=self.viernes,
            sabado=self.sabado,
            domingo=self.domingo
        )
        alimentacion = Alimentacion(
            id_usuario=self.id_usuario,
            numero_semanas=self.numero_semanas ,
            plan_alimentacion = plan_alimentacion
        )

        db.session.add(alimentacion)
        db.session.commit()
        return alimentacion

    # Función que retorna la recomendación de entrenamiento
    def execute(self):
        try:
            # Logica de negocio
            response = consumir_servicio_usuarios(self.headers)
            validar_permisos_usuario(response)
            alimentacion = self.registrar_plan_nutricional_bd()            
            return alimentacion_schema.dump(alimentacion)
        except IntegrityError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)
        except SQLAlchemyError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)