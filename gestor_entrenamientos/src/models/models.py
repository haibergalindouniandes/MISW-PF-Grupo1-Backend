# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Creación de variable db
db = SQLAlchemy()
class Entrenamientos(db.Model):
    __tablename__ = 'entrenamientos'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entrenamiento = db.Column(db.String, nullable=False)
    numero_semanas = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    # Relación uno a uno con la tabla PlanEntrenamiento
    plan_entrenamiento = db.relationship('PlanEntrenamiento', uselist=False, back_populates='entrenamiento')
       
class PlanEntrenamiento(db.Model):
    __tablename__ = "plan_entrenamiento"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lunes = db.Column(db.Integer, nullable=False)
    martes = db.Column(db.Integer, nullable=False)
    miercoles = db.Column(db.Integer, nullable=False)
    jueves = db.Column(db.Integer, nullable=False)
    viernes = db.Column(db.Integer, nullable=False)
    sabado = db.Column(db.Integer, nullable=False)
    domingo = db.Column(db.Integer, nullable=False)        
    # Relación uno a uno con la tabla Entrenamientos
    entrenamiento_id = db.Column(UUID(as_uuid=True), db.ForeignKey('entrenamientos.id'))
    entrenamiento = db.relationship('Entrenamientos', back_populates='plan_entrenamiento')
    
class ResultadosEntrenamiento(db.Model):
    __tablename__ = 'resultados_entrenamiento'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    actividad = db.Column(db.String(32), nullable=False)
    vo2max = db.Column(db.Float(precision=32), nullable=True)
    ftp = db.Column(db.Float(precision=32), nullable=True)
    tiempo = db.Column(db.Time, nullable=False)
    retroalimentacion = db.Column(db.String(32), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    id_usuario = db.Column(db.String, nullable=False)

class ResultadosEntrenamientoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ResultadosEntrenamiento
        id = fields.String()

class PlanEntrenamientoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlanEntrenamiento
        include_relationships = True     

class EntrenamientoSchema(SQLAlchemyAutoSchema):
    plan_entrenamiento = fields.Nested(PlanEntrenamientoSchema)
    class Meta:
        model = Entrenamientos
        include_relationships = True
        load_instance = True
   