import uuid
from src.main import app
from faker import Faker
import random
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
    response_healthcheck = {}
    response_create_user = {}

    def set_up(self):
        self.usuario = self.dataFactory.email()
        self.contrasena = self.dataFactory.password(length=10, special_chars=True, upper_case=True, lower_case=True, digits=True)
        self.nombres = self.dataFactory.name()
        self.peso = random.uniform(40,500) #random.randint(40, 500)
        self.apellidos = self.dataFactory.name()
        self.edad = random.randint(18, 90)
        self.tipo_documento = "CC"
        self.altura = random.uniform(130,230)  #random.randint(130, 230)        
        self.numero_documento = str(self.dataFactory.random_int(10000000, 99999999))
        self.pais_nacimiento=self.dataFactory.country()
        self.ciudad_nacimiento = self.dataFactory.country()
        self.genero = "M"
        self.pais_residencia = self.dataFactory.country()
        self.ciudad_residencia = self.dataFactory.country()
        self.deportes = ['Ciclismo', 'Atletismo']
        self.antiguedad = random.randint(1, 900)
        self.tipo_plan = "Basico"
        self.tipo_usuario = "Deportista"

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

    def execute_healthcheck(self):
        with app.test_client() as test_client:
            self.response_healthcheck = test_client.get('/usuarios/ping')

    def execute_create_user(self, data):
        with app.test_client() as test_client:
                self.response_create_user = test_client.post('/usuarios', json=data)

    def test_validar_healthcheck(self):
        self.execute_healthcheck()
        assert self.response_healthcheck.status_code == 200
        
    def test_validar_create_user(self):
        self.set_up()
        self.execute_create_user(self.data)
        assert self.response_create_user.status_code == 200    
   