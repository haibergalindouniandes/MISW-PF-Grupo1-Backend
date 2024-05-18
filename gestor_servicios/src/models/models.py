# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Creación de variable db
db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos de Usuario
class Notificaciones(db.Model):
    __tablename__ = "notificaciones"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario = db.Column(db.String(100), nullable=True)
    latitud = db.Column(db.String(200), nullable=True)
    longitud = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.String(200), nullable=True)
    tipo = db.Column(db.String(30), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Función que retorna un diccionario a partir del modelo
    def to_dict(self):
        return {
            "id": str(self.id),
            "usuario": self.name,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "descripcion": self.descripcion,
            "tipo": self.tipo,
            "fecha_creacion": int(self.fecha_creacion),
            "fecha_actualizacion": float(self.fecha_actualizacion)
        }

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

    # Función que retorna un diccionario a partir del modelo
    def to_dict(self):
        return {
                    "id": str(self.id),
                    "nombre": self.nombre,
                    "descripcion": self.descripcion,
                    "frecuencia": self.frecuencia,
                    "costo": self.costo,
                    "numero_minimo_participantes": self.numero_minimo_participantes,
                    "numero_maximo_participantes": self.numero_maximo_participantes,
                    "lugar": self.lugar,
                    "fecha": str(self.fecha),
                    "id_usuario": self.id_usuario,
                    "horario": self.horario,
                    "estado": self.estado
                }

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

    # Función que retorna un diccionario a partir del modelo
    def to_dict(self):
        return {
                    "id": str(self.id),
                    "id_usuario": self.id_usuario,
                    "id_servicio": self.id_servicio,
                    "email": self.email,
                    "fecha": self.fecha,
                    "hora": self.hora
                }