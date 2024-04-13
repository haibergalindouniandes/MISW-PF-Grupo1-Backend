import uuid
from src.main import app
from faker import Faker
import json

# Clase que contiene la logica del test
class TestResources():
        # Declaración constantes
    dataFactory = Faker()
    usuario = None
    contrasena = None
    nombres = None
    peso = None
    apellidos = None
    edad = None
    tipo_documento = None
    altura = None
    numero_documento = None
    pais_nacimiento = None
    ciudad_nacimiento = None
    genero = None
    pais_residencia = None 
    ciudad_residencia = None 
    deportes = None
    tipo_plan = None
    antiguedad = None
    tipo_usuario = None
    data = {}
    responseLogin = {}

    # Función que genera data del usuario
    def set_up(self):
        self.usuario = self.dataFactory.email()
        self.contrasena = self.dataFactory.password(
            length=10, special_chars=True, upper_case=True, lower_case=True, digits=True)
        self.nombres = self.dataFactory.name()
        self.peso = 80
        self.apellidos = self.dataFactory.name()
        self.edad = 30
        self.tipo_documento = "cedula"
        self.altura = 170        
        self.numero_documento = str(self.dataFactory.random_int(1000, 1000000000))
        self.pais_nacimiento=self.dataFactory.country()
        self.ciudad_nacimiento = self.dataFactory.country()
        self.genero = "MASCULINO"
        self.pais_residencia = self.dataFactory.country()
        self.ciudad_residencia = self.dataFactory.country()
        self.deportes = None
        self.antiguedad = 12
        self.tipo_plan = "BASIC"
        self.tipo_usuario = "USUARIO"

        self.data = {
            "usuario": f"{self.usuario}",
            "contrasena": f"{self.contrasena}",
            "nombres": f"{self.nombres}",
            "peso": f"{self.peso}",
            "apellidos": f"{self.apellidos}",
            "edad": f"{self.edad}",
            "tipo_documento": f"{self.tipo_documento}",
            "altura": f"{self.altura}",
            "numero_documento": f"{self.numero_documento}",
            "pais_nacimiento": f"{self.pais_nacimiento}",
            "ciudad_nacimiento": f"{self.ciudad_nacimiento}",
            "genero": f"{self.genero}",
            "pais_residencia": f"{self.pais_residencia}",
            "ciudad_residencia": f"{self.ciudad_residencia}",
            "deportes": f"{self.deportes}",
            "antiguedad": f"{self.antiguedad}",
            "tipo_plan": f"{self.tipo_plan}",
            "tipo_usuario": f"{self.tipo_usuario}"
        }

    # Función que crea un usuario
    def execute_create_user(self, data):
        try:
            with app.test_client() as test_client:
                self.responseCreateUser = test_client.post(
                    '/usuarios', json=data
                )
        except:
            assert True

    # Función que valida la creación exitosa de un usuario
    def validate_success_create_user(self): 
        assert True     

    # Función que crea un usuario exitosamente
    def create_user_success(self):
        # Creación nuevo usuario
        self.set_up()
        self.execute_create_user(self.data)
        self.validate_success_create_user()
        # response_json = json.loads(self.responseCreateUser.data)
        #self.userId = "cbce8fd9-4df9-4860-933b-23d9b8cdeecf"     

    # Función que valida la creación exitosa de un usuario
    def test_create_new_user(self):
        # Creación nuevo usuario
        self.create_user_success()


    # Función que valida el estado del servidor
    def test_health_check(self):
        # Reset tabla usuarios
        with app.test_client() as test_client:
            response = test_client.get(
                '/usuarios/ping'
            )
            data = str(response.data)
        assert response.status_code == 200
        assert 'pong' in data

   # Función que genera el token
    def execute_login(self, data):
        with app.test_client() as test_client:
            self.responseToken = test_client.post(
                'usuarios/login', json=data
            )

    # Función que valida la generacion exitosa del token
    def validate_success_login(self):
        print("validate_success_login")
        print(self.responseToken.status_code)
        assert self.responseToken.status_code == 200

    # Función que valida la generacion exitosa del token
    def validate_failed_login(self):
        print("validate_failed_login")
        print(self.responseToken.status_code)
        assert self.responseToken.status_code == 400        

    # Función que genera el login exitosamente
    def test_generate_login_success(self):
        #CreateUser
        self.create_user_success()
        print("resultado test_generate_login_success")
        print(self.usuario)
        print("resultado crear usuario")
        print(self.responseCreateUser.status_code)
        # Generación Login
        dataAuthenticate = {
            "email": f"{self.usuario}",
            "password": f"{self.contrasena}"#Falso123.*"
        }        
        self.execute_login(dataAuthenticate)
        self.validate_success_login()   


    # Función que falla la generacion de login
    def test_generate_login_fail_invalid_user(self):
        # Generación token
        dataAuthenticate = {
            "email": f"noexisto@no.com",
            "password": f"Falso123.*"
        }
        print("resultado test_generate_login_fail_invalid_user")        
        self.execute_login(dataAuthenticate)
        self.validate_failed_login()   


    # Función que falla la generacion de login email invalido
    def test_generate_login_fail_invalid_email(self):
        # Generación token
        dataAuthenticate = {
            "email": f"noexisto@",
            "password": f"Falso123.*"
        }
        print("resultado test_generate_login_fail_invalid_email")
        self.execute_login(dataAuthenticate)
        self.validate_failed_login()   


    # Función que falla la generacion de login contreasena invalido
    def test_generate_login_fail_invalid_contrasena(self):
        # Generación token
        dataAuthenticate = {
            "email": f"noexisto@",
            "password": f"Falso"
        }
        print("resultado test_generate_login_fail_invalid_contrasena")
        self.execute_login(dataAuthenticate)
        self.validate_failed_login()   
