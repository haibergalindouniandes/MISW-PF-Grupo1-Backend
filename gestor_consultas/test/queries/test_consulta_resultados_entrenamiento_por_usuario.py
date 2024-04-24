import random
import requests
from datetime import datetime
from faker import Faker
from src.errors.errors import BadRequest, NoRecordsFound, TokenNotFound
from src.queries.consultar_resultado_entrenamiento_por_usuario import ConsultarResultadoEntrenamientoPorUsuario
import src.main

class TestConsultarResultadoEntrenamientoPorUsuario:
    # Declaración constantes
    dataFactory = Faker()    
    data = {}
    headers = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}     
        self.id_usuario = "031ea802-fe54-11ee-8470-01e0aa2bcd86"
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

    # Función que valida el request invalido
    def test_validar_request_invalido(self):
        try:
            self.set_up()
            id_usuario = None
            ConsultarResultadoEntrenamientoPorUsuario(id_usuario, self.headers).query()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description
            
   # Función que valida cuando no se envia el token
    def test_validar_token_no_enviado(self):
        try:
            self.set_up()
            ConsultarResultadoEntrenamientoPorUsuario(self.id_usuario, {}).query()
        except Exception as e:
            assert e.code == TokenNotFound.code
            
    # Función que valida cuando el token es invalido
    def test_validar_token_invalido(self):
        try:
            self.set_up()
            headers = {}
            headers["Authorization"] = "token_invalido"
            ConsultarResultadoEntrenamientoPorUsuario(self.id_usuario, headers).query()
        except Exception as e:
            assert e.code == BadRequest.code
            assert e.description == BadRequest.description              
            
    # Función que valida la consulta de informacion con un usaurio no existente
    def test_validar_id_usuario_inexistente(self):
        try:
            self.set_up()
            id_usuario = "00000000-0000-0000-0000-000000000000"
            ConsultarResultadoEntrenamientoPorUsuario(id_usuario, self.headers).query()
        except Exception as e:
            assert e.code == NoRecordsFound.code
            assert e.description == NoRecordsFound.description