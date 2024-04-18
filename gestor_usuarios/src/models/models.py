# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
from marshmallow import fields, Schema
import uuid
import json

# Creación de variable db
db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos de Usuario
class Usuario(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid1)
    usuario = db.Column(db.String(128), primary_key=True, nullable=False)
    contrasena = db.Column(db.String(64), nullable=False)
    nombres = db.Column(db.String(32), nullable=False)
    peso = db.Column(db.Float(precision=32), nullable=False)
    apellidos = db.Column(db.String(32), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    tipo_documento = db.Column(db.String(16), nullable=False)
    altura = db.Column(db.Float(precision=32), nullable=False)
    numero_documento = db.Column(db.String(16), nullable=False)
    pais_nacimiento = db.Column(db.String(64), nullable=False)
    ciudad_nacimiento = db.Column(db.String(64), nullable=False)
    genero = db.Column(db.String(8), nullable=False)
    pais_residencia = db.Column(db.String(64), nullable=False)
    ciudad_residencia = db.Column(db.String(64), nullable=False)
    deportes = db.Column(JSONB, nullable=False)
    antiguedad = db.Column(db.Integer, nullable=False)
    tipo_plan = db.Column(db.String(32), nullable=False)
    tipo_usuario = db.Column(db.String(32), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Función que retorna un diccionario a partir del modelo
    def to_dict(self):
        return {
            "id": str(self.id),
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "nombres": self.nombres,
            "peso": float(self.peso),
            "apellidos": self.apellidos,
            "edad": int(self.edad),
            "tipo_documento": self.tipo_documento,
            "altura": float(self.altura),
            "numero_documento": self.numero_documento,
            "pais_nacimiento": self.pais_nacimiento,
            "ciudad_nacimiento": self.ciudad_nacimiento,
            "genero": self.genero,
            "pais_residencia": self.pais_residencia,
            "ciudad_residencia": self.ciudad_residencia,
            "deportes": self.deportes,
            "antiguedad": int(self.antiguedad),
            "tipo_plan": self.tipo_plan,
            "tipo_usuario": self.tipo_usuario
        }