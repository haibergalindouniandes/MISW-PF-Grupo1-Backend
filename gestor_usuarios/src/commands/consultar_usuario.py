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
            result = db.session.query(Usuario).filter_by(usuario = self.email, contrasena = contrasena_encriptada).first()
            if result!=None:

                logging.info("resultado")
                logging.info(result)
                logging.info(result.id)
                logging.info(result.nombres)
                usuario = Usuario(
                    id=result.id,
                    usuario=result.usuario,
                    contrasena=result.contrasena,
                    nombres=result.nombres,
                    peso=result.peso,
                    apellidos=result.apellidos,
                    edad=result.edad,
                    tipo_documento=result.tipo_documento,
                    altura=result.altura,                    
                    numero_documento=result.numero_documento,
                    pais_nacimiento=result.pais_nacimiento,
                    ciudad_nacimiento=result.ciudad_nacimiento,
                    genero=result.genero,
                    pais_residencia=result.pais_residencia,
                    ciudad_residencia=result.ciudad_residencia,
                    deportes=result.deportes,
                    antiguedad=result.antiguedad,
                    tipo_plan=result.tipo_plan,
                    tipo_usuario=result.tipo_usuario,
                    fecha_creacion=result.fecha_creacion,
                    fecha_actualizacion=result.fecha_actualizacion                                   
                )
                logging.info(usuario)
            else:
                raise LoginFailed()
            return usuario
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
