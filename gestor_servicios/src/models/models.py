# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime
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
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Función que retorna un diccionario a partir del modelo
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "descripcion": self.descripcion,
            "tipo": self.tipo,
            "create_date": int(self.create_date),
            "update_date": float(self.update_date)
        }