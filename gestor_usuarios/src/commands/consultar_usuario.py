import asyncio
import traceback
from commands.base_command import BaseCommannd
#from utilities.utilities import booleano_a_string, obtener_endpoint_entrenamientos, obtener_endpoint_plan_nutricional, agregar_servicio_a_batch, limpiar_batch_de_servicios, ejecucion_batch_en_paralelo, string_a_booleano
from models.models import db, Usuario
#from validators.validators import validar_esquema, esquema_registro_usuario
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError
from models.models import Usuario



# Clase que contiene la logica de consulta de usuarios
class ConsultarUsuario(BaseCommannd):
    email: str
    password_encriptado: str

    # Constructor
    def __init__(self, data):
        self.email=data["email"]
        self.password_encriptado=data["password"]
    
    # Función que realiza de consulta de un usuario
    def execute(self):
        try:
            # Logica de negocio
            usuario = Usuario.query.filter(Usuario.email == self.email,
                                Usuario.password == self.password_encriptado).first()
            return usuario
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
