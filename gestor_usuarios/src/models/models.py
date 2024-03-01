# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Creación de variable db
db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos de Usuario
class Usuario(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=True)
    tipo_identificacion = db.Column(db.String(30), nullable=True)
    numero_identificacion = db.Column(db.String(30), nullable=True)
    sexo = db.Column(db.String(30), nullable=True)
    edad = db.Column(db.Integer, nullable=True)
    peso = db.Column(db.Numeric(precision=5, scale=2), nullable=True)
    estatura = db.Column(db.Numeric(precision=5, scale=2), nullable=True)
    enfermedades_cardiovasculares = db.Column(db.Boolean, default=False)
    pais = db.Column(db.String(50), nullable=True)
    departamento = db.Column(db.String(90), nullable=True)
    ciudad = db.Column(db.String(90), nullable=True)
    id_entrenamiento = db.Column(db.String(90), nullable=True)
    id_plan_nutricional = db.Column(db.String(90), nullable=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)

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
            "id_entrenamiento": self.id_entrenamiento,
            "id_plan_nutricional": self.id_plan_nutricional,
            "create_date": str(self.create_date),
            "update_date": str(self.update_date)
        }