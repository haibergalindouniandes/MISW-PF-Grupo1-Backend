import random
from faker import Faker
import requests
from src.main import app

class TestResources:
    # Declaración constantes
    dataFactory = Faker()   
    headers = {}
    response_healthcheck = {}
    response_token = {}
    response_consulta_plan_alimentacion_por_usuario = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}
        self.id_usuario = "50e4d92c-fdef-11ee-8470-01e0aa2bcd86"
        self.ejecucion_generar_token(data_login)
        self.headers["Authorization"] = f"Bearer {self.response_token['token']}"
    
    # Función consume el API de generación del token
    def ejecucion_generar_token(self, data):
        url = "https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/login"             
        response = requests.post(url, json=data)
        self.response_token  = response.json()

    # Función consume el API de generación de healthcheck de entrenamientos
    def ejecucion_healthcheck(self):
        with app.test_client() as test_client:
            self.response_healthcheck = test_client.get('/consultas/ping')
    
    # Función consume el API de consulta de plan de entrenamiento por usuario
    def ejecucion_consultar_plan_alimentacion_por_usuario(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_plan_alimentacion_por_usuario = test_client.get(f"/consultas/plan-alimentacion/usuario/{self.id_usuario}", headers=headers)    
    
    # Función que valida el healthcheck
    def test_validar_healthcheck(self):
        self.ejecucion_healthcheck()
        assert self.response_healthcheck.status_code == 200

    # # Función que valida consulta
    def test_validar_consulta_plan_alimentacion_por_usuario(self):
        self.set_up()
        self.ejecucion_consultar_plan_alimentacion_por_usuario(self.headers)
        assert self.response_consulta_plan_alimentacion_por_usuario.status_code == 200
        
   