# MISW4501-2024-Grupo1
Repositorio del Grupo 1 de la Materia de Proyecto Final 2024 MISW4501

## Integrantes:

|   Nombre                         |   Correo                      | Codigo    | 
|----------------------------------|-------------------------------|-----------|
| Jhon Fredy Guzmán Caicedo        | jf.guzmanc1@uniandes.edu.co   | 202216872 |
| Haiber Humberto Galindo Sanchez  | h.galindos@uniandes.edu.co    | 202216850 |
| Jorge M. Carrillo                | jm.carrillo@uniandes.edu.co   | 200426097 |
| Shiomar Alberto Salazar Castillo | s.salazarc@uniandes.edu.co    | 202213359 |

## Microservicios Implementados
### Gestor Plan Nutricional
## Estructura de las Carpeta del proyecto
```
microservice
├── src/ => Carpeta que contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio.
│	├── main.py => Contiene la configuración base del microservicio.
│	├── blueprints => Contiene la exposición de los recursos ofrecidos por el microservicio.
│	├── commands => Contiene la lógica de las funcionalidades y comunicación con la capa de persistencia.
│	├── errors => Contiene la configuración de los errores que se mostrarán al usuario.
│	├── models => Contiene la configuración de los modelos que se utilizarán para la creación de las tablas en la base de datos.
│	├── querys => Contiene la implementacion base para la creacion de Consultas, inserts, updates.
│	├── utilities => Contiene las funcionalidades utilitarias del servicio.
│	└── validators => Contiene las funcionalidades que validan diferentes procesos del servicio.
└── tests/ => Carpeta que contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/src`.
	├── conftest.py => Contiene la configuración base de las pruebas.
	├── blueprints => Contiene las pruebas enfocadas en la capa de exposición del servicio.
```

### Gestor de Entrenamientos
## Estructura de las Carpeta del proyecto
```
microservice
├── src/ => Carpeta que contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio.
│	├── main.py => Contiene la configuración base del microservicio.
│	├── blueprints => Contiene la exposición de los recursos ofrecidos por el microservicio.
│	├── commands => Contiene la lógica de las funcionalidades y comunicación con la capa de persistencia.
│	├── errors => Contiene la configuración de los errores que se mostrarán al usuario.
│	├── models => Contiene la configuración de los modelos que se utilizarán para la creación de las tablas en la base de datos.
│	├── querys => Contiene la implementacion base para la creacion de Consultas, inserts, updates.
│	├── utilities => Contiene las funcionalidades utilitarias del servicio.
│	└── validators => Contiene las funcionalidades que validan diferentes procesos del servicio.
└── tests/ => Carpeta que contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/src`.
	├── conftest.py => Contiene la configuración base de las pruebas.
	├── blueprints => Contiene las pruebas enfocadas en la capa de exposición del servicio.
```

### Gestor de Usuarios

## Estructura de las Carpeta del proyecto
```
microservice
├── src/ => Carpeta que contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio.
│	├── main.py => Contiene la configuración base del microservicio.
│	├── blueprints => Contiene la exposición de los recursos ofrecidos por el microservicio.
│	├── commands => Contiene la lógica de las funcionalidades y comunicación con la capa de persistencia.
│	├── errors => Contiene la configuración de los errores que se mostrarán al usuario.
│	├── models => Contiene la configuración de los modelos que se utilizarán para la creación de las tablas en la base de datos.
│	├── querys => Contiene la implementacion base para la creacion de Consultas, inserts, updates.
│	├── utilities => Contiene las funcionalidades utilitarias del servicio.
│	└── validators => Contiene las funcionalidades que validan diferentes procesos del servicio.
└── tests/ => Carpeta que contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/src`.
	├── conftest.py => Contiene la configuración base de las pruebas.
	├── blueprints => Contiene las pruebas enfocadas en la capa de exposición del servicio.
```
### Gestor de Servicios


## Estructura de las Carpeta del proyecto

```
microservice
├── src/ => Carpeta que contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio.
│	├── main.py => Contiene la configuración base del microservicio.
│	├── blueprints => Contiene la exposición de los recursos ofrecidos por el microservicio.
│	├── commands => Contiene la lógica de las funcionalidades y comunicación con la capa de persistencia.
│	├── errors => Contiene la configuración de los errores que se mostrarán al usuario.
│	├── models => Contiene la configuración de los modelos que se utilizarán para la creación de las tablas en la base de datos.
│	├── utilities => Contiene las funcionalidades utilitarias del servicio.
│	└── validators => Contiene las funcionalidades que validan diferentes procesos del servicio.
└── tests/ => Carpeta que contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/src`.
	├── conftest.py => Contiene la configuración base de las pruebas.
	├── blueprints => Contiene las pruebas enfocadas en la capa de exposición del servicio.
	└── commands => Contiene las pruebas enfocadas en la capa lógica del servicio.
```
