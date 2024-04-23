# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import DeclarativeBase

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


ma = Marshmallow()
class ConsultaPlanAlimentacionPorUsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id_usuario', 'numero_semanas', 'fecha_creacion', 'fecha_actualizacion', 'alimentacion_id', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo')






