# Importación de dependencias
import asyncio
import traceback
from commands.base_command import BaseCommannd
from models.models import db, Usuario
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.errors import ApiError, UserAlreadyRegistered
import hashlib


class RegistrarUsuario(BaseCommannd):
    # Constructor
    def __init__(self, data):        
        self.asignar_datos_usuario(data)

    # Función que valida el request del servicio
    def asignar_datos_usuario(self, json_payload):
        # Asignacion de variables
        self.usuario = json_payload['usuario']
        self.contrasena = hashlib.md5(json_payload['contrasena'].encode('utf-8')).hexdigest()
        self.nombres = json_payload['nombres']
        self.peso = float(json_payload['peso'])
        self.apellidos = json_payload['apellidos']
        self.edad = int(json_payload['edad'])
        self.tipo_documento = json_payload['tipo_documento']
        self.altura = float(json_payload['altura'])
        self.numero_documento = json_payload['numero_documento']
        self.pais_nacimiento = json_payload['pais_nacimiento']
        self.ciudad_nacimiento = json_payload['ciudad_nacimiento']
        self.genero = json_payload['genero']
        self.pais_residencia = json_payload['pais_residencia']
        self.ciudad_residencia = json_payload['ciudad_residencia']
        self.deportes = json_payload['deportes']
        self.antiguedad = int(json_payload['antiguedad'])
        self.tipo_plan = json_payload['tipo_plan']
        self.tipo_usuario = json_payload['tipo_usuario']

    # Función que realiza el registro del usuario en BD
    def registrar_usuario_bd(self):
        # Registrar en BD
        usuario = Usuario(
            usuario = self.usuario,
            contrasena = self.contrasena,
            nombres = self.nombres,
            peso = self.peso,
            apellidos = self.apellidos,
            edad = self.edad,
            tipo_documento = self.tipo_documento,
            altura = self.altura,
            numero_documento = self.numero_documento,
            pais_nacimiento = self.pais_nacimiento,
            ciudad_nacimiento = self.ciudad_nacimiento,
            genero = self.genero,
            pais_residencia = self.pais_residencia,
            ciudad_residencia = self.ciudad_residencia,
            deportes = self.deportes,
            antiguedad = self.antiguedad,
            tipo_plan = self.tipo_plan,
            tipo_usuario = self.tipo_usuario            
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    # Función que realiza creación de la Alerta
    def execute(self):
        try:            
            usuario_registrado = self.registrar_usuario_bd().to_dict()            
            return usuario_registrado
        except IntegrityError as e:# pragma: no cover
            db.session.rollback()
            raise UserAlreadyRegistered(e)
        except SQLAlchemyError as e:# pragma: no cover
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)