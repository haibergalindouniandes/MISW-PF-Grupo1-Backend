

from datetime import datetime, timedelta
from faker import Faker
from src.errors.errors import BadRequest, Forbidden, TokenNotFound, Unauthorized
from src.commands.registrar import RegistrarServicio
import requests
import random
import src.main

class TestRegistrar:
    # Declaración constantes
    data_factory = Faker()    
    data = {}
    headers = {}

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

    # Función que permite generar una fecha futura
    def generar_fecha_futura(self, dias):
        fecha_actual = datetime.now()
        fecha_futura = fecha_actual + timedelta(days=dias)
        return fecha_futura.strftime('%Y-%m-%d')
        
    # Función que consume el API de generación del token
    def ejecucion_generar_token(self, data):
        url = "https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/login"             
        response = requests.post(url, json=data)
        json_response = response.json()
        token = json_response["token"]
        self.headers["Authorization"] = f"Bearer {token}"
        
    # Función que valida el request invalido
    def test_validar_request_invalido(self):
        try:
            self.set_up()
            data = self.data
            del data["nombre"]
            RegistrarServicio(data, self.headers).execute()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description
            
    # Función que valida cuando no se envia el token
    def test_validar_token_no_enviado(self):
        try:
            self.set_up()
            RegistrarServicio(self.data, {}).execute()
        except Exception as e:
            assert e.code == TokenNotFound.code
            assert e.description == TokenNotFound.description
    
    # Función que valida cuando el token es invalido
    def test_validar_token_invalido(self):
        try:
            self.set_up()
            headers = {}
            headers["Authorization"] = "token_invalido"
            RegistrarServicio(self.data, headers).execute()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description  

   # Función que valida cuando se presenta un error de tipo Unauthorized
    def test_validar_error_no_autorizado(self):
        try:
            self.set_up()
            headers = {}
            headers["Authorization"] = f"{self.headers['Authorization']}invalido"
            RegistrarServicio(self.data, headers).execute()
        except Exception as e:
            assert e.code == Unauthorized.code
            assert e.description == Unauthorized.description

    # Función que valida cuando se presenta un error de tipo Forbidden
    def test_validar_error_no_tiene_permisos(self):
        try:
            self.set_up()
            data_login = {"email": "cliente0001@gmail.com", "password": "cliente0001"}   
            self.ejecucion_generar_token(data_login)    
            RegistrarServicio(self.data, self.headers).execute()
        except Exception as e:
            assert e.code == Forbidden.code
            assert e.description == Forbidden.description
            
    # Función que valida el registro exitoso de un servicio
    def test_registrar_servicio(self):
        self.set_up()
        response = RegistrarServicio(self.data, self.headers).execute()
        assert response != None
        assert response["id_usuario"] == self.data["id_usuario"]
        assert response["nombre"] == self.data["nombre"]
        assert response["descripcion"] == self.data["descripcion"]
        assert response["frecuencia"] == self.data["frecuencia"]
        assert response["costo"] == self.data["costo"]
        assert response["lugar"] == self.data["lugar"]            
        