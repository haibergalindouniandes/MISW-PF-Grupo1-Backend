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
    response_consulta_resultados_entrenamiento_por_usuario = {}
    response_consulta_usuario = {}
    response_consulta_servicios = {}
    response_consulta_detalle_servicio = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}
        self.id_usuario = "8e8239b0-0762-11ef-89fc-2b0cac54c9b4"
        self.id_servicio = "98f2a2e9-e396-412b-a4ca-0c0cab729c27"
        self.ejecucion_generar_token(data_login)
        self.headers["Authorization"] = f"Bearer {self.response_token['token']}"
    
    # Función consume el API de generación del token
    def ejecucion_generar_token(self, data):
        url = "https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/login"
        response = requests.post(url, json=data)
        self.response_token  = response.json()

    # Función consume el API de generación de healthcheck del servicio consultas
    def ejecucion_healthcheck(self):
        with app.test_client() as test_client:
            self.response_healthcheck = test_client.get('/consultas/ping')
    
    # Función consume el API de consulta de plan de alimentacion por usuario
    def ejecucion_consultar_plan_alimentacion_por_usuario(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_plan_alimentacion_por_usuario = test_client.get(f"/consultas/plan-alimentacion/usuario/{self.id_usuario}", headers=headers)

    # Función consume el API de consulta de resultados de entrenamiento por usuario
    def ejecucion_consultar_resultados_entrenamiento_por_usuario(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_resultados_entrenamiento_por_usuario = test_client.get(f"/consultas/resultado-entrenamiento/usuario/{self.id_usuario}", headers=headers)

    # Función consume el API de consulta de usuario
    def ejecucion_consultar_usuario(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_usuario = test_client.get(f"/consultas/usuarios/me", headers=headers)

    # Función consume el API de consulta de servicios
    def ejecucion_consultar_servicios(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_servicios = test_client.get(f"/consultas/servicios", headers=headers)

    # Función consume el API de consulta de detalle de servicio
    def ejecucion_consultar_detalle_servicio(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_detalle_servicio = test_client.get(f"/consultas/servicios/{self.id_servicio}", headers=headers)

    # Función que valida el healthcheck
    def test_validar_healthcheck(self):
        self.ejecucion_healthcheck()
        assert self.response_healthcheck.status_code == 200

    # Función que valida consulta de plan de alimentacion por usuario
    def test_validar_consulta_plan_alimentacion_por_usuario(self):
        self.set_up()
        self.ejecucion_consultar_plan_alimentacion_por_usuario(self.headers)
        assert self.response_consulta_plan_alimentacion_por_usuario.status_code == 200

    # Función que valida consulta de resultados de entrenamiento por usuario
    def test_validar_consulta_resultados_entrenamiento_por_usuario(self):
        self.set_up()
        self.ejecucion_consultar_resultados_entrenamiento_por_usuario(self.headers)
        assert self.response_consulta_resultados_entrenamiento_por_usuario.status_code == 200

    # Función que valida consulta usuario
    def test_validar_consulta_de_usuario(self):
        self.set_up()
        self.ejecucion_consultar_usuario(self.headers)
        assert self.response_consulta_usuario.status_code == 200

    # Función que valida consulta de servicios
    def test_validar_consulta_servicios(self):
        self.set_up()
        self.ejecucion_consultar_servicios(self.headers)
        assert self.response_consulta_servicios.status_code == 200

    # Función que valida consulta del detalle de un servicio
    def test_validar_consulta_detalle_servicio(self):
        self.set_up()
        self.ejecucion_consultar_detalle_servicio(self.headers)
        assert self.response_consulta_detalle_servicio.status_code == 200

        
   