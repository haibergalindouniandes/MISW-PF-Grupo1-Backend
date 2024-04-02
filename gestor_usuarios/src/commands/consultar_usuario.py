import asyncio
import traceback
from commands.base_command import BaseCommannd
#from utilities.utilities import booleano_a_string, obtener_endpoint_entrenamientos, obtener_endpoint_plan_nutricional, agregar_servicio_a_batch, limpiar_batch_de_servicios, ejecucion_batch_en_paralelo, string_a_booleano
from models.models import db, Usuario
#from validators.validators import validar_esquema, esquema_registro_usuario
from sqlalchemy.exc import SQLAlchemyError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema
from errors.errors import ApiError, LoginFailed
from models.models import Usuario
import hashlib
import logging



# Clase que contiene la logica de consulta de usuarios
class ConsultarUsuario(BaseCommannd):
    email: str
    password: str

    # Constructor
    def __init__(self, data):
        self.email=data["email"]
        self.password=data["password"]
    
    # Función que realiza de consulta de un usuario
    def execute(self):
        try:
            logging.info("Execute Consultar  Usuario")
            logging.info(self)
            # Logica de negocio
            contrasena_encriptada = hashlib.md5(self.password.encode('utf-8')).hexdigest()
            #result = db.session.query(Usuario).filter_by(email = self.email,
            #                    password = contrasena_encriptada).first()
            #result= Usuario.query.filter(Usuario.email == self.email,
            #                    Usuario.password == contrasena_encriptada).first()
            result = db.session.query(Usuario).filter_by(email = self.email, password = contrasena_encriptada).first()
            if result!=None:

                logging.info("resultado")
                logging.info(result)
                logging.info(result.id)
                logging.info(result.nombres)
                usuario = Usuario(
                    id=result.id,
                    nombres=result.nombres,
                    apellidos=result.apellidos,
                    tipo_identificacion=result.tipo_identificacion,
                    numero_identificacion=result.numero_identificacion,
                    sexo=result.sexo,
                    edad=result.edad,
                    peso=result.peso,
                    estatura=result.estatura,
                    enfermedades_cardiovasculares=result.enfermedades_cardiovasculares,
                    pais=result.pais,
                    departamento=result.departamento,
                    ciudad=result.ciudad,
                    email=result.email,
                    password=result.password,
                    rol=result.rol,
                    plan=result.plan
                )
                logging.info(usuario)
            else:
                raise LoginFailed()
            return usuario
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
