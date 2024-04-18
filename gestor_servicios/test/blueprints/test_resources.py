import random
import requests
from faker import Faker
from datetime import datetime, timedelta
from src.main import app

class TestResources:
    # Declaración constantes
    data_factory = Faker()    
    data = {}
    headers = {}
    response_healthcheck = {}
    response_token = {}
    response_registro_servicio = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "prestador2024@uniandes.edu.co", "password": "Prestador2*24"}    
        lista_frecuencia = ['Diario', 'Semanal', 'Mensual', 'Trimestral','Semestral', 'Anual']    
        id_usuario = "6da46c66-f5ee-11ee-a0c6-c9ae58811c0e"
        self.ejecucion_generar_token(data_login) 
        
        lugar = self.data_factory.street_address()
        fecha_futura = self.generar_fecha_futura(3)
        self.data = {
            "nombre": f"{self.data_factory.name()}",
            "descripcion": f"Carrera benefica a favor de los niños de cancer, se iniciara en {lugar} atravesando diversas calles.",
            "frecuencia": f"{random.choice(lista_frecuencia)}",
            "costo": f"{round(random.uniform(10000, 100000), 2)} COP",
            "numero_minimo_participantes": random.randint(1, 10),
            "numero_maximo_participantes": random.randint(11, 40),
            "lugar": f"{lugar}",
            "fecha": f"{fecha_futura}",
            "horario": [
                "8:00:00 a. m.",
                "9:00:00 a. m.",
                "10:00:00 a. m.",
                "11:00:00 a. m.",
                "12:00:00 p. m.",
                "1:00:00 p. m.",
                "2:00:00 p. m.",
                "3:00:00 p. m.",
                "4:00:00 p. m.",
                "5:00:00 p. m."
            ],
            "id_usuario": f"{id_usuario}"
        }
        
        self.headers["Authorization"] = f"Bearer {self.response_token['token']}"
    
    # Función que permite generar una fecha futura
    def generar_fecha_futura(self, dias):
        fecha_actual = datetime.now()
        fecha_futura = fecha_actual + timedelta(days=dias)
        return fecha_futura.strftime('%Y-%m-%d')
    
    # Función que consume el API de generación del token
    def ejecucion_generar_token(self, data):
        url = "https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/login"             
        response = requests.post(url, json=data)
        self.response_token  = response.json()

    # Función que consume el API de generación de healthcheck de entrenamientos
    def ejecucion_healthcheck(self):
        with app.test_client() as test_client:
            self.response_healthcheck = test_client.get(
                '/servicios/ping'
            )
    
    # Función que consume el API de registro de servicios
    def ejecucion_registrar_servicio(self, data, headers):
        with app.test_client() as test_client:
            self.response_registro_servicio = test_client.post(
                '/servicios', json=data, headers=headers
            )    
    
    # Función que valida el healthcheck
    def test_validar_healthcheck(self):
        self.ejecucion_healthcheck()
        assert self.response_healthcheck.status_code == 200
        
    # Función que valida el registro exitoso de un servicio
    def test_validar_registro_servicio(self):
        self.set_up()
        self.ejecucion_registrar_servicio(self.data, self.headers)
        assert self.response_registro_servicio.status_code == 200