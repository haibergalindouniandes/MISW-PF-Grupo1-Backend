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

class PlanNutricional(db.Model):
    __tablename__ = 'PlanNutricional'
    id = db.Column(db.Integer, primary_key=True)
    plan_nutricional = db.Column(db.String(50), unique=True)
    menus = db.Column(JSONB)    
    proposito = db.Column(db.String(50))
    clasificacion = db.Column(db.String(50))

class PlanNutricionalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlanNutricional
        id = fields.String()