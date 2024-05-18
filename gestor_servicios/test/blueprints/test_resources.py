import random
import requests
from faker import Faker
from datetime import datetime, timedelta
from src.main import app

class TestResources:
    # Declaración constantes
    data_factory = Faker()    
    data = {}
    data_agendar_login_success = {}
    data_update_agendar_success = {}
    data_agendar_service_not_found = {}
    headers = {}
    response_healthcheck = {}
    response_token = {}
    response_registro_servicio = {}
    response_agendar_servicio = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "prestador2024@uniandes.edu.co", "password": "Prestador2*24"}    
        lista_frecuencia = ['Diario', 'Semanal', 'Mensual', 'Trimestral','Semestral', 'Anual']    
        id_usuario = "e3ade316-124e-11ef-a39e-612ef9f72f01"
        self.ejecucion_generar_token(data_login) 
        
        lugar = self.data_factory.city()
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
        
        self.data_agendar = {
            "id_usuario":f"{id_usuario}",
            "id_servicio":"5c9395df-314d-4205-ac8b-ef8e9cece867",
            "email":"prestador2024@uniandes.edu.co",
            "fecha":f"{fecha_futura}",
            "hora":"12:01:01"
        }

        self.headers["Authorization"] = f"Bearer {self.response_token['token']}"
    
    # Función que genera data inicial
    def set_up2(self): 
        data_agendar_login_success = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}           
        self.ejecucion_generar_token(data_agendar_login_success) 
        id_usuario='fafc3900-124e-11ef-a39e-612ef9f72f01'
        fecha_futura = self.generar_fecha_futura(2)

        self.data_agendar_success = {
            "id_usuario":f"{id_usuario}",
            "id_servicio":"5c9395df-314d-4205-ac8b-ef8e9cece867",
            "email":"usuario2024@uniandes.edu.co",
            "fecha":f"{fecha_futura}",
            "hora":"12:01:01"
        }

        print(self.data_agendar_success)
        print(self.headers)
        print(self.response_token)

        self.data_update_agendar_success= {
            "id_usuario":f"{id_usuario}",
            "id_servicio":"5c9395df-314d-4205-ac8b-ef8e9cece867",
            "email":"usuario2024@uniandes.edu.co",
            "fecha":f"{fecha_futura}",
            "hora":"12:01:01"
        }

        print(self.data_update_agendar_success)
        print(self.headers)
        print(self.response_token)


        self.headers["Authorization"] = f"Bearer {self.response_token['token']}"
        print(self.data_agendar_success)
        print(self.headers)
        print(self.response_token)

    # Función que genera data inicial
    def set_up3(self): 
        data_agendar_login_success = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}           
        self.ejecucion_generar_token(data_agendar_login_success) 
        id_usuario='fafc3900-124e-11ef-a39e-612ef9f72f01'
        fecha_futura = self.generar_fecha_futura(2)

        self.data_agendar_service_not_found = {
            "id_usuario":f"{id_usuario}",
            "id_servicio":"fafc3900-124e-11ef-a39e-612ef9f72f01",
            "email":"usuario2024@uniandes.edu.co",
            "fecha":f"{fecha_futura}",
            "hora":"12:01:01"
        }

        self.headers["Authorization"] = f"Bearer {self.response_token['token']}"
        print(self.data_agendar_service_not_found)
        print(self.headers)
        print(self.response_token)


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
    def ejecucion_agendar_servicio(self, data, headers):
        with app.test_client() as test_client:
            self.response_agendar_servicio = test_client.post(
                '/servicios/agendar', json=data, headers=headers
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


    # Función que valida el registro exitoso de un servicio
    def test_validar_agenda_servicio_fail(self):
        self.set_up()
        self.ejecucion_agendar_servicio(self.data_agendar, self.headers)
        assert self.response_agendar_servicio.status_code == 403

    # Función que valida el registro exitoso de un servicio
    def test_validar_update_agenda_servicio(self):
        self.set_up2()
        self.ejecucion_agendar_servicio(self.data_agendar_success, self.headers)
        self.ejecucion_agendar_servicio(self.data_update_agendar_success, self.headers)
        print('################################')
        print(self.response_agendar_servicio)
        assert self.response_agendar_servicio.status_code == 200


    # Función que valida el registro exitoso de un servicio
    def test_validar_agenda_servicio_not_found(self):
        self.set_up3()
        self.ejecucion_agendar_servicio(self.data_agendar_service_not_found, self.headers)
        assert self.response_agendar_servicio.status_code == 400

