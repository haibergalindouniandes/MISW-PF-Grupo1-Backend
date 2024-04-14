import uuid
from faker import Faker
from src.commands.registrar_usuario import RegistrarUsuario
import random
import hashlib
import src.main
import json

class TestResources():       
    dataFactory = Faker()
    usuario = None
    contrasena = None
    nombres = None
    peso = None
    apellidos = None
    edad = None
    tipo_documento = None
    altura = None
    numero_documento = None
    pais_nacimiento = None
    ciudad_nacimiento = None
    genero = None
    pais_residencia = None 
    ciudad_residencia = None 
    deportes = None
    tipo_plan = None
    antiguedad = None
    tipo_usuario = None
    data = {}


    def set_up(self):
        self.usuario = self.dataFactory.email()
        self.contrasena = self.dataFactory.password(length=10, special_chars=True, upper_case=True, lower_case=True, digits=True)
        self.nombres = self.dataFactory.name()
        self.peso = random.randint(40, 500)
        self.apellidos = self.dataFactory.name()
        self.edad = random.randint(18, 90)
        self.tipo_documento = "CC"
        self.altura = random.randint(130, 230)        
        self.numero_documento = str(self.dataFactory.random_int(10000000, 99999999))
        self.pais_nacimiento=self.dataFactory.country()
        self.ciudad_nacimiento = self.dataFactory.country()
        self.genero = "M"
        self.pais_residencia = self.dataFactory.country()
        self.ciudad_residencia = self.dataFactory.country()
        self.deportes = ['Ciclismo', 'Atletismo']
        self.antiguedad = random.randint(1, 900)
        self.tipo_plan = "Basico"
        self.tipo_usuario = "Usuario"

        self.data = {
            "usuario": f"{self.usuario}",
            "contrasena": f"{self.contrasena}",
            "nombres": f"{self.nombres}",
            "peso": self.peso,
            "apellidos": f"{self.apellidos}",
            "edad": self.edad,
            "tipo_documento": f"{self.tipo_documento}",
            "altura": self.altura,
            "numero_documento": f"{self.numero_documento}",
            "pais_nacimiento": f"{self.pais_nacimiento}",
            "ciudad_nacimiento": f"{self.ciudad_nacimiento}",
            "genero": f"{self.genero}",
            "pais_residencia": f"{self.pais_residencia}",
            "ciudad_residencia": f"{self.ciudad_residencia}",
            "deportes": self.deportes,
            "antiguedad": self.antiguedad,
            "tipo_plan": f"{self.tipo_plan}",
            "tipo_usuario": f"{self.tipo_usuario}"
        }

    def test_create_user(self):
        self.set_up()
        response = RegistrarUsuario(self.data).execute()
        assert response != None
        assert response["usuario"] == self.data["usuario"]
        assert response["contrasena"] == hashlib.md5(self.data["contrasena"].encode('utf-8')).hexdigest()
        assert response["nombres"] == self.data["nombres"]
        assert response["peso"] == self.data["peso"]
        assert response["apellidos"] == self.data["apellidos"]
        assert response["edad"] == self.data["edad"]
        assert response["tipo_documento"] == self.data["tipo_documento"]
        assert response["altura"] == self.data["altura"]
        assert response["numero_documento"] == self.data["numero_documento"]
        assert response["pais_nacimiento"] == self.data["pais_nacimiento"]
        assert response["ciudad_nacimiento"] == self.data["ciudad_nacimiento"]
        assert response["genero"] == self.data["genero"]
        assert response["pais_residencia"] == self.data["pais_residencia"]
        assert response["ciudad_residencia"] == self.data["ciudad_residencia"]
        assert response["deportes"] == self.data["deportes"]
        assert response["antiguedad"] == self.data["antiguedad"]
        assert response["tipo_plan"] == self.data["tipo_plan"]
        assert response["tipo_usuario"] == self.data["tipo_usuario"]
