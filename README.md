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
### Flujo de Trabajo
Para este repositorio se utilizara un proceso de GitFlow Modificado, en donde se tendran 3  tipos de ramas:

* Rama ```main```: Rama principal en donde vivira el codigo mas actualizado y sincronizado de todos los microservicios, la cual esta protegida para que solo mediante un Pull Request Validado se pueda meter nuevo codigo.
* Ramas ``` hotfix_``` en donde estan los cambios menores o correcciones realizadas despues de hacer merge de una las ramas de Historias de Usuario.
* Ramas de ```feature_{nombre_microservicio}``` Ramas para el desarrollo de las Historias de Usuario planeadas por cada microservicio.

En el siguiente diagrama se puede observar este Flujo de Trabajo:

![FlujoTrabajo_Movil](https://github.com/shiomar-salazar/MISW-PF-Grupo1-Movil/assets/111320185/f6505f8f-2835-4306-be84-0fe2806e23e1)

### Flujo de Integracion y Despliegue Continuo:
Para este reppsitorio se tiene implementado un sistema de CI/CD basado en GitHub, CloudBuild - CGP y Cloud Run - GCP , consistendo de las siguientes caracteristicas:

* * La integracion Continua arranca de dos formas
  * cada que exista un n. evo Pull Request a la rama ```main```.
  * cada que segenere un push hacia la rama feature_{n. mbre:microservicio}.
* La integracion continua hace un build de cada microservicio correspondiente a su rama.
* Si el build es exitoso procede a crear la imagen del contenerdor para ese microservicio.
* Si la imagen se crea exitosamente se procede a cargarla en el container-registry de GCP.
* Si la carga es exitosa, se continua con el deploy en cloud Run y redireccion detrafico a la nueva implementacion realizada.
