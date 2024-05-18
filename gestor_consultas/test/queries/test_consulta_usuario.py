import random
import requests
from datetime import datetime
from faker import Faker
from src.errors.errors import BadRequest, NoRecordsFound, TokenNotFound
from src.queries.consultar_usuario import ConsultarUsuario
import src.main

class TestConsultarUsuario:
    # Declaración constantes
    dataFactory = Faker()    
    data = {}
    headers = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}        
        self.ejecucion_generar_token(data_login) 
        
    # Función que permite obtener la fecha actual
    def obtener_fecha_actual(self):
        fecha_actual = datetime.now()
        return fecha_actual.strftime('%Y-%m-%d')
    
    # Función consume el API de generación del token
    def ejecucion_generar_token(self, data):
        url = "https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/login"             
        response = requests.post(url, json=data)
        json_response = response.json()
        token = json_response["token"]
        self.headers["Authorization"] = f"Bearer {token}"

  # Función que valida cuando no se envia el token
    def test_validar_token_no_enviado(self):
        try:
            self.set_up()
            ConsultarUsuario({}).query()
        except Exception as e:
            assert e.code == TokenNotFound.code
            
    # Función que valida cuando el token es invalido
    def test_validar_token_invalido(self):
        try:
            self.set_up()
            headers = {}
            headers["Authorization"] = "token_invalido"
            ConsultarUsuario(headers).query()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description              
            
   