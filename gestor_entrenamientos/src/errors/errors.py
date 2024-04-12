# Clase que contiene la estructura de error por defecto
class ApiError(Exception):
    code = 500
    description = "Error interno, por favor revise el log"

# Clase que contiene la estructura de un error de tipo Bad Request
class CallExternalServiceError(ApiError):
    code = 500
    description = "Error al consumir servicio externo, por favor revise los logs."  

# Clase que contiene la estructura de un error de tipo Bad Request
class BadRequest(ApiError):
    code = 400
    description = "Párametros de entrada invalidos, por favor revise los logs."

# Clase que contiene la estructura de un error de tipo Unauthorized
class Unauthorized(ApiError):
    code = 401
    description = "El token proporcionado no es valido o esta vencido, por favor valide e intente nuevamente."

# Clase que contiene la estructura de un error de tipo TokenNotFound
class TokenNotFound(ApiError):
    code = 401
    description = "El token es obligatorio, por favor valide e intente nuevamente."

# Clase que contiene la estructura de un error de tipo Forbidden    
class Forbidden(ApiError):
    code = 403
    description = "No esta autorizado para realizar esta operación, por favor valide con el administrador del sistema."      

# Clase que contiene la estructura de un error cuando se encuentra información del plan de entrenamiento
class TrainingPlanNotFound(ApiError):
    code = 404
    description = "No se encontro información con los parámetros ingresados, por favor valide e intente nuevamente."  
    
# Clase que contiene la estructura de un error de tipo id_usuario debe ser unico
class TrainingPlanAlreadyRegistered(ApiError):
    code = 409
    description = "Ya se encuentra registrado un plan de entrenamiento con usuario ingresado, por favor valide e intente nuevamente."      