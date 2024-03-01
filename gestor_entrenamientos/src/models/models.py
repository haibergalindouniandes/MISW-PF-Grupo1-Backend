# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
import uuid

# Creación de variable db
db = SQLAlchemy()

class Entrenamientos(db.Model):
    __tablename__ = 'entrenamientos'
    id = db.Column(db.Integer, primary_key=True)
    rutina = db.Column(db.String(50), unique=True)
    ejercicios = db.Column(JSONB)
    tipo_entrenamiento = db.Column(db.String(50))
    proposito = db.Column(db.String(50))
    clasificacion = db.Column(db.String(50))

class EntrenamientosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entrenamientos
        id = fields.String()