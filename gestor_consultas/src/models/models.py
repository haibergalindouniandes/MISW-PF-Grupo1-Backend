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


class ResultadosEntrenamiento(db.Model):
    __tablename__ = 'resultados_entrenamiento'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    actividad = db.Column(db.String(32), nullable=False)
    distancia = db.Column(db.Float(precision=32), nullable=False)
    vo2max = db.Column(db.Float(precision=32), nullable=True)
    ftp = db.Column(db.Float(precision=32), nullable=True)
    tiempo = db.Column(db.Time, nullable=False)
    retroalimentacion = db.Column(db.String(32), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    id_usuario = db.Column(db.String, nullable=False)



ma = Marshmallow()
class ConsultaPlanAlimentacionPorUsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id_usuario', 'numero_semanas', 'fecha_creacion', 'fecha_actualizacion', 'alimentacion_id', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo')


class ConsultaResultadosEntrenamientoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ResultadosEntrenamiento
        id = fields.String()




