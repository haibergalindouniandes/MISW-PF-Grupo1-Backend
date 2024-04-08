import traceback
from queries.base_query import BaseQuery
from models.models import db, Usuario
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, LoginFailed
from models.models import Usuario
import hashlib

# Clase que contiene la logica de inicio de sesión
class IniciarSesion(BaseQuery):
    email: str
    password: str

    # Constructor
    def __init__(self, data):
        self.email=data["email"]
        self.password=data["password"]
    
    # Función que realiza el inicio de sesión del usuario
    def query(self):
        try:
            # Logica de negocio
            contrasena_encriptada = hashlib.md5(self.password.encode('utf-8')).hexdigest()
            usuario = db.session.query(Usuario).filter_by(usuario = self.email, contrasena = contrasena_encriptada).first()
            if usuario == None:
                raise LoginFailed
            return usuario
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        
