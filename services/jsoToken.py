import jwt
from datetime import datetime, timedelta

class TokenManager:
    SECRET_KEY = 'clavesecretacambiar'  # Esta es la clave secreta que usaremos para firmar los tokens
    ALGORITHM = 'HS256'              # Algoritmo de firma

    @classmethod
    def generar_token(cls, cedula,rol, expiracion_horas=24):

        ahora = datetime.now()
        expiracion = ahora + timedelta(hours=expiracion_horas)
        payload = {
            'id': cedula,  
            'rol': rol,                # 'sub' se refiere al sujeto del token (el usuario)       
            'iat': ahora,                   # Fecha de emisión
            'exp': expiracion               # Fecha de expiración
        }
        token = jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def validar_token(cls, token):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload  # El payload contendrá información como 'sub', 'iat', 'exp'
        except jwt.ExpiredSignatureError:
            # El token ha expirado
            return None
        except jwt.InvalidTokenError:
            # El token es inválido por alguna razón
            return None
