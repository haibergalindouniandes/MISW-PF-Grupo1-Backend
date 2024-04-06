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

# Creación de variable db
db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos de Usuario
class Usuario(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario = db.Column(db.String(100), nullable=False, default=None)
    contrasena = db.Column(db.String(250), nullable=False, default=None)
    nombres = db.Column(db.String(100), nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    tipo_documento = db.Column(db.String(30), nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    numero_documento = db.Column(db.String(30), nullable=False)
    pais_nacimiento = db.Column(db.String(50), nullable=False)
    ciudad_nacimiento = db.Column(db.String(90), nullable=False)
    genero = db.Column(db.String(30), nullable=False)
    pais_residencia = db.Column(db.String(50), nullable=False)
    ciudad_residencia = db.Column(db.String(90), nullable=False)
    deportes = db.Column(JSONB, nullable=False)
    antiguedad = db.Column(db.Integer, nullable=False)
    tipo_plan = db.Column(db.String(30), nullable=False)
    tipo_usuario = db.Column(db.String(30), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Función que retorna un diccionario a partir del modelo
    def to_dict(self):
        return {
            "id": str(self.id),
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "tipo_identificacion": self.tipo_identificacion,
            "numero_identificacion": self.numero_identificacion,
            "sexo": self.sexo,
            "edad": int(self.edad),
            "peso": float(self.peso),
            "estatura": float(self.estatura),
            "enfermedades_cardiovasculares": bool(self.enfermedades_cardiovasculares),
            "pais": self.pais,
            "departamento": self.departamento,
            "ciudad": self.ciudad,
            "fecha_creacion": str(self.fecha_creacion),
            "fecha_actualizacion": str(self.fecha_actualizacion),
            "email": str(self.email),
            "password": str(self.password),
            "rol": str(self.rol),
            "plan": str(self.plan)
        }