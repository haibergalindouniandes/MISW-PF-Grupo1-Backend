from cryptography.fernet import Fernet

def generar_clave():
    # Generar una clave
    return Fernet.generate_key()

def exportar_clave_a_archivo(clave, archivo='clave.key'):
    # Escribir la clave en un archivo
    with open(archivo, 'wb') as archivo_clave:
        archivo_clave.write(clave)

def cargar_clave_desde_archivo(archivo='clave.key'):
    # Leer la clave desde un archivo
    with open(archivo, 'rb') as archivo_clave:
        clave = archivo_clave.read()
    return clave

def cifrar_texto(texto, clave):
    cipher_suite = Fernet(clave)
    texto_cifrado = cipher_suite.encrypt(texto.encode())
    return texto_cifrado

def descifrar_texto(texto_cifrado, clave):
    cipher_suite = Fernet(clave)
    texto_descifrado = cipher_suite.decrypt(texto_cifrado).decode()
    return texto_descifrado
