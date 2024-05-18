import random
import pytest
import requests
from src.utilities.utilities import obtener_endpoint_usuarios
from src.commands.registrar_resultados_entrenamiento import RegistrarResultadosEntrenamiento
from src.errors.errors import BadRequest, Forbidden, TokenNotFound, Unauthorized
from faker import Faker
import src.main
from datetime import datetime


class TestCrearPlanEntrenamiento:
    # Declaración constantes
    dataFactory = Faker()    
    data = {}
    headers = {}
    
    # Función que genera data inicial
    def obtener_token(self, data):
        url = "https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/login"             
        response = requests.post(url, json=data)
        json_response = response.json()
        token = json_response["token"]
        self.headers["Authorization"] = f"Bearer {token}"
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}   
        json_response = self.obtener_token(data_login)
        lista_entrenamientos = ["Ciclismo", "Atletismo"]
        lista_retroalimentacion = ["Bien", "Excelente"]    
        id_usuario = "6da46c66-f5ee-11ee-a0c6-c9ae58811c0e"
        
        
        self.data = {
            "actividad": f"{random.choice(lista_entrenamientos)}",
            "distancia": random.randint(1, 10),
            "ftp": random.randint(100, 500),
            "vo2max": random.randint(10, 90),
            "tiempo": f"0{random.randint(1, 9)}:0{random.randint(1, 9)}:0{random.randint(1, 9)}",
            "retroalimentacion": f"{random.choice(lista_retroalimentacion)}",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "id_usuario": f"{id_usuario}"            
        }
        
        
    
    # Función que valida el request invalido
    def test_validar_request_invalido(self):
        try:
            self.set_up()
            data = self.data
            del data["actividad"]
            RegistrarResultadosEntrenamiento(data, self.headers).execute()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description
            
    # Función que valida cuando no se envia el token
    def test_validar_token_no_enviado(self):
        try:
            self.set_up()
            data = self.data
            RegistrarResultadosEntrenamiento(data, {}).execute()
        except Exception as e:
            assert e.code == TokenNotFound.code
            assert e.description == TokenNotFound.description

   # Función que valida cuando el token es invalido
    def test_validar_token_invalido(self):
        try:
            self.set_up()
            headers = {}
            headers["Authorization"] = "token_invalido"
            RegistrarResultadosEntrenamiento(self.data, headers).execute()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description            

    # Función que valida cuando se presenta un error de tipo Unauthorized
    def test_validar_error_no_autorizado(self):
        try:
            self.set_up()
            RegistrarResultadosEntrenamiento(self.data, self.headers).execute()
        except Exception as e:
            assert e.code == Unauthorized.code
            assert e.description == Unauthorized.description
    
    # Función que valida cuando se presenta un error de tipo Forbidden
    def test_validar_error_no_tiene_permisos(self):
        try:
            self.set_up()
            data_login = {"email": "prestador2024@uniandes.edu.co", "password": "Prestador2*24"}   
            self.obtener_token(data_login)    
            RegistrarResultadosEntrenamiento(self.data, self.headers).execute()
        except Exception as e:
            assert e.code == Forbidden.code
            assert e.description == Forbidden.description
    
    # Función que valida la creación exitosa de un plan de entrenamiento
    def test_crear_plan_entrenamiento(self):
        self.set_up()
        response = RegistrarResultadosEntrenamiento(self.data, self.headers).execute()
        assert response != None
        assert response["actividad"] == self.data["actividad"]
        if self.data["actividad"] == "Ciclismo":
            assert response["ftp"] == self.data["ftp"]
        elif self.data["actividad"] == "Atletismo":
            assert response["vo2max"] == self.data["vo2max"]    
        assert response["distancia"] == self.data["distancia"]
        assert response["retroalimentacion"] == self.data["retroalimentacion"]
        assert response["fecha"] == self.data["fecha"]
        assert response["tiempo"] == self.data["tiempo"]
        assert response["id_usuario"] == self.data["id_usuario"]
