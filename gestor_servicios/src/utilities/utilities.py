# Función que valida el request para la creación de usuarios
def formatDateTimeToUTC(dateTime):
    return dateTime.split('.')[0].replace(' ', 'T')