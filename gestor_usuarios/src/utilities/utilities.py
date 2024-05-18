import os
import traceback
import jwt
import datetime
from errors.errors import ApiError, LoginFailed, ExpiredToken, InvalidEmail,InvalidContrasena
import re

JWT_SECRET_KEY =  os.environ["JWT_SECRET_KEY"]
def generar_token(data):
    try:
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        payload = {
            'id_usuario': str(data.id),
            'exp': expiration_time
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        traceback.print_exc()
        raise ApiError
    
def validar_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        exp = payload['exp']
        exp_datetime = datetime.datetime.utcfromtimestamp(exp)
        now = datetime.datetime.utcnow()
        if now > exp_datetime:
            raise ExpiredToken
        return payload
    except jwt.ExpiredSignatureError:
        raise ExpiredToken
    except jwt.InvalidTokenError:
        raise LoginFailed

def is_valid_email(email):
    # Regular expression for validating an Email
    regex = r'^[a-zA-Z0-9-_\.]+@([a-zA-Z0-9-_]+\.)+[a-zA-Z0-9-_]{2,4}$'
    # If the string matches the regex, it is a valid email
    if re.match(regex, email):
        return True
    else:
        raise InvalidEmail
    
def is_valid_contrasena(contrasena):
    # Regular expression for validating an Email
    regex = r'^(?!.* )(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$'
    # If the string matches the regex, it is a valid email
    if re.match(regex, contrasena):
        return True
    else:
        raise InvalidContrasena