# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Creación de variable db
db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos de Usuario
class Notificaciones(db.Model):
    __tablename__ = "notificaciones"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=True)
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
            "name": self.name,
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
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    frecuencia = db.Column(db.String, nullable=False)
    costo = db.Column(db.String, nullable=False)
    numero_minimo_participantes = db.Column(db.Integer, nullable=False)
    numero_maximo_participantes = db.Column(db.Integer, nullable=False)
    lugar = db.Column(db.String, nullable=True)
    fecha = db.Column(db.DateTime, nullable=False)
    id_usuario = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, default='ACT')
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
                    "estado": self.estado
                }