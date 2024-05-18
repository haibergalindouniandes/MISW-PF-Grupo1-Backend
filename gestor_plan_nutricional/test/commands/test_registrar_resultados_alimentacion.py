import random
import requests
from datetime import datetime
from faker import Faker
from src.errors.errors import BadRequest, Forbidden, TokenNotFound, Unauthorized
from src.commands.registrar_resultados_alimentacion import RegistrarResultadosAlimentacion
import src.main

class TestRegistrarResultadosAlimentacion:
    # Declaración constantes
    dataFactory = Faker()    
    data = {}
    headers = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}     
        id_usuario = "d0d85122-eafd-11ee-a951-0242ac120002"
        fecha_actual = self.obtener_fecha_actual()
        self.ejecucion_generar_token(data_login) 
        
        self.data = {
            "calorias_1": f"{random.randint(300, 400)}",
            "calorias_2": f"{random.randint(300, 400)}",
            "calorias_3": f"{random.randint(300, 400)}",
            "ml_agua": f"{random.randint(300, 400)}",
            "fecha": f"{fecha_actual }",
            "id_usuario": f"{id_usuario}"
        }
        
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

    # Función que valida el request invalido
    def test_validar_request_invalido(self):
        try:
            self.set_up()
            data = self.data
            del data["id_usuario"]
            RegistrarResultadosAlimentacion(data, self.headers).execute()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description
            
   # Función que valida cuando no se envia el token
    def test_validar_token_no_enviado(self):
        try:
            self.set_up()
            RegistrarResultadosAlimentacion(self.data, {}).execute()
        except Exception as e:
            assert e.code == TokenNotFound.code
            
    # Función que valida cuando el token es invalido
    def test_validar_token_invalido(self):
        try:
            self.set_up()
            headers = {}
            headers["Authorization"] = "token_invalido"
            RegistrarResultadosAlimentacion(self.data, headers).execute()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description

   # Función que valida cuando se presenta un error de tipo Unauthorized
    def test_validar_error_no_autorizado(self):
        try:
            self.set_up()
            headers = {}
            headers["Authorization"] = f"{self.headers['Authorization']}invalido"
            RegistrarResultadosAlimentacion(self.data, headers).execute()
        except Exception as e:
            assert e.code == Unauthorized.code
            assert e.description == Unauthorized.description

    # Función que valida cuando se presenta un error de tipo Forbidden
    def test_validar_error_no_tiene_permisos(self):
        try:
            self.set_up()
            data_login = {"email": "prestador2024@uniandes.edu.co", "password": "Prestador2*24"}   
            self.ejecucion_generar_token(data_login)    
            RegistrarResultadosAlimentacion(self.data, self.headers).execute()
        except Exception as e:
            assert e.code == Forbidden.code
            assert e.description == Forbidden.description            