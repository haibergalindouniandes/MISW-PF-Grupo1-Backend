# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB, JSON
from sqlalchemy import UniqueConstraint
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
    contactos_emergencia = db.Column(JSONB, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

class Servicios(db.Model):
    __tablename__ = "servicios"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(600), nullable=False)
    frecuencia = db.Column(db.String(100), nullable=False)
    costo = db.Column(db.String(100), nullable=False)
    numero_minimo_participantes = db.Column(db.Integer, nullable=False)
    numero_maximo_participantes = db.Column(db.Integer, nullable=False)
    lugar = db.Column(db.String(600), nullable=True)
    fecha = db.Column(db.DateTime, nullable=False)
    horario = db.Column(JSON, nullable=False)
    id_usuario = db.Column(db.String(36), nullable=False)
    estado = db.Column(db.String(10), default='ACT')
    # Llave compuesta
    __table_args__ = (
        UniqueConstraint('nombre', 'fecha', 'id_usuario', name='ck_servicio_fecha_usuario'),
    )

class AgendaServicios(db.Model):
    __tablename__ = "agendas"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_usuario = db.Column(db.String, nullable=False)
    id_servicio = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow) 
    # Llave compuesta
    __table_args__ = (
        UniqueConstraint('id', 'id_usuario', 'id_servicio','fecha', name='ck_agenda_servicio_fecha_usuario'),
    )

ma = Marshmallow()
class ConsultaPlanAlimentacionPorUsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id_usuario', 'numero_semanas', 'fecha_creacion', 'fecha_actualizacion', 'alimentacion_id', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo')


class ConsultaResultadosEntrenamientoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ResultadosEntrenamiento
        id = fields.String()

class ConsultaUsuariosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        id = fields.String()

class ConsultaServiciosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'costo', 'lugar')

class ConsultaDetalleServicioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Servicios
        id = fields.String()

class ConsultaServiciosPorUsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'costo', 'lugar', 'fecha', 'nombre_proveedor', 'descripcion', 'nombre_usuario')

class ConsultaServiciosAgendadosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'costo', 'lugar', 'fecha', 'horario', 'descripcion', 'nombre_usuario')
        
class ConsultaUsuariosAgendadosServicioSchema(ma.Schema):
    class Meta:
        fields = ('id_usuario', 'nombre_usuario', 'email', 'fecha', 'hora', 'pais_residencia', 'ciudad_residencia')        