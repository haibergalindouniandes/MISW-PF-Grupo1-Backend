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

class Alimentacion(db.Model):
    __tablename__ = 'alimentacion'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    id_usuario = db.Column(db.String, nullable=False)
    numero_semanas = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow) 
    # Relación uno a uno con la tabla PlanAlimentacion
    plan_alimentacion = db.relationship('PlanAlimentacion', uselist=False, back_populates='alimentacion')
    

class PlanAlimentacion(db.Model):
    __tablename__ = "plan_alimentacion"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lunes = db.Column(db.Integer, nullable=False)
    martes = db.Column(db.Integer, nullable=False)
    miercoles = db.Column(db.Integer, nullable=False)
    jueves = db.Column(db.Integer, nullable=False)
    viernes = db.Column(db.Integer, nullable=False)
    sabado = db.Column(db.Integer, nullable=False)
    domingo = db.Column(db.Integer, nullable=False)        
    # Relación uno a uno con la tabla Alimentacion
    alimentacion_id = db.Column(UUID(as_uuid=True), db.ForeignKey('alimentacion.id'))
    alimentacion = db.relationship('Alimentacion', back_populates='plan_alimentacion')
    
class PlanAlimentacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlanAlimentacion
        include_relationships = True     

class AlimentacionSchema(SQLAlchemyAutoSchema):
    plan_alimentacion = fields.Nested(PlanAlimentacionSchema)
    class Meta:
        model = Alimentacion
        include_relationships = True
        load_instance = True
   

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