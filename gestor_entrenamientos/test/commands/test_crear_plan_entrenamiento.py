import random
from unittest.mock import MagicMock, patch

import pytest
import requests
from src.utilities.utilities import obtener_endpoint_usuarios
from src.commands.crear_plan_entrenamiento import CrearPlanEntrenamiento
from src.errors.errors import BadRequest, Forbidden, TokenNotFound, Unauthorized
from faker import Faker
import src.main

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
        data_login = {"email": "cliente0001@gmail.com", "password": "cliente0001"}   
        json_response = self.obtener_token(data_login)
        lista_entrenamientos = [ "Ciclismo", "Carreras" ]    
        id_usuario = "6da46c66-f5ee-11ee-a0c6-c9ae58811c0e"
        
        
        self.data = {
            "entrenamiento": f"{random.choice(lista_entrenamientos)}",
            "numero_semanas": random.randint(1, 10),
            "id_usuario": f"{id_usuario}",
            "plan_entrenamiento": {
                "lunes": f"{random.randint(1, 10)}",
                "martes": f"{random.randint(1, 10)}",
                "miercoles": f"{random.randint(1, 10)}",
                "jueves": f"{random.randint(1, 10)}",
                "viernes": f"{random.randint(1, 10)}",
                "sabado": f"{random.randint(1, 10)}",
                "domingo": f"{random.randint(1, 10)}"
            }
        }
        
        
    
    # Función que valida el request invalido
    def test_validar_request_invalido(self):
        try:
            self.set_up()
            data = self.data
            del data["plan_entrenamiento"]
            CrearPlanEntrenamiento(data, self.headers).execute()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description
            
    # Función que valida cuando no se envia el token
    def test_validar_token_no_enviado(self):
        try:
            self.set_up()
            data = self.data
            CrearPlanEntrenamiento(data, {}).execute()
        except Exception as e:
            assert e.code == TokenNotFound.code
            assert e.description == TokenNotFound.description

   # Función que valida cuando el token es invalido
    def test_validar_token_invalido(self):
        try:
            self.set_up()
            headers = {}
            headers["Authorization"] = "token_invalido"
            CrearPlanEntrenamiento(self.data, headers).execute()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description            

    # Función que valida cuando se presenta un error de tipo Unauthorized
    def test_validar_error_no_autorizado(self):
        try:
            self.set_up()
            CrearPlanEntrenamiento(self.data, self.headers).execute()
        except Exception as e:
            assert e.code == Unauthorized.code
            assert e.description == Unauthorized.description
    
    # Función que valida cuando se presenta un error de tipo Forbidden
    def test_validar_error_no_tiene_permisos(self):
        try:
            self.set_up()
            data_login = {"email": "prestador0001", "password": "prestador0001"}   
            self.obtener_token(data_login)    
            CrearPlanEntrenamiento(self.data, self.headers).execute()
        except Exception as e:
            assert e.code == Forbidden.code
            assert e.description == Forbidden.description
    
    # Función que valida la creación exitosa de un plan de entrenamiento
    def test_crear_plan_entrenamiento(self):
        self.set_up()
        response = CrearPlanEntrenamiento(self.data, self.headers).execute()
        assert response != None
        assert response["entrenamiento"] == self.data["entrenamiento"]
        assert response["id_usuario"] == self.data["id_usuario"]
        assert response["numero_semanas"] == self.data["numero_semanas"]