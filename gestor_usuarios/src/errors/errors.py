# Clase que contiene la estructura de error por defecto
class ApiError(Exception):
    code = 500
    description = "Error interno, por favor revise el log"

# Clase que contiene la estructura de un error de tipo Bad Request
class BadRequest(ApiError):
    code = 400
    description = "Párametros de entrada invalidos"

# Clase que contiene la estructura de un error de tipo Bad Request
class InvalidEmail(ApiError):
    code = 400
    description = "Email Invalido"    


# Clase que contiene la estructura de un error de tipo Bad Request
class InvalidContrasena(ApiError):
    code = 400
    description = "Contrasena Invalido"    

# Clase que contiene la estructura de un error cuando el login falla
class LoginFailed(ApiError):
    code = 400
    description = "Inicio de sesión fallido, corrija los datos ingresados e intente nuevamente."    

# Clase que contiene la estructura de un error cuando el token esta expirado
class ExpiredToken(ApiError):
    code = 401
    description = "El token ha expirado, por favor vuelva a iniciar sesión."    

class TokenNotFound(ApiError):
    code = 401
    description = "El token es obligatorio, por favor valide e intente nuevamente."

# Clase que contiene la estructura de un error cuando el login falla
class UserNotFound(ApiError):
    code = 404
    description = "El usuario ingresado no se encuentre registrado, por favor valide e intente nuevamente."    

# Clase que contiene la estructura de un error de tipo Usuario debe ser unico
class UserAlreadyRegistered(ApiError):
    code = 409
    description = "El usuario ingresado ya se encuentra registrado, por favor valide e intente nuevamente."