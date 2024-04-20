# Clase que contiene la estructura de error por defecto
class ApiError(Exception):
    code = 500
    description = "Error interno, por favor revise el log"

# Clase que contiene la estructura de un error de tipo Bad Request
class BadRequest(ApiError):
    code = 400
    description = "Párametros de entrada invalidos"
    
# Clase que contiene la estructura de un error de tipo Bad Request
class ErrorConsumoServicioExterno(ApiError):
    code = 500
    description = "Error al consumir servicio externo"    
    
# Clase que contiene la estructura de un error de tipo Bad Request
class ErrorMetodoNoPermitido(ApiError):
    code = 409
    description = "Metodo no permitido"        

# Clase que contiene la estructura de un error de tipo Bad Request
class LoginFailed(ApiError):
    code = 400
    description = "Login Failed, corrija los datos ingresados e intente nuevamente."    

# Clase que contiene la estructura de un error de tipo Usuario debe ser unico
class UserAlreadyRegistered(ApiError):
    code = 409
    description = "El usuario ingresado ya se encuentra registrado, por favor valide e intente nuevamente."