# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
import uuid

# Creación de variable db
db = SQLAlchemy()

# class PlanNutricional(db.Model):
#     __tablename__ = 'plan_nutricional'
#     id = db.Column(db.Integer, primary_key=True)
#     plan_nutricional = db.Column(db.String(50), unique=True)
#     menus = db.Column(JSONB)    
#     proposito = db.Column(db.String(50))
#     clasificacion = db.Column(db.String(50))

# class PlanNutricionalSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = PlanNutricional
#         id = fields.String()
        
class ResultadosAlimentacion(db.Model):
    __tablename__ = 'resultados_alimentacion'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    calorias_1 = db.Column(db.Integer, nullable=False)
    calorias_2 = db.Column(db.Integer, nullable=False)
    calorias_3 = db.Column(db.Integer, nullable=False)
    ml_agua = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    id_usuario = db.Column(db.String, nullable=False)

class ResultadosAlimentacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ResultadosAlimentacion
        id = fields.String()        