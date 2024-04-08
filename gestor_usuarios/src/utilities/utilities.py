import os
import traceback
import jwt
import datetime
from errors.errors import ApiError, LoginFailed, ExpiredToken

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