import bcrypt
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from ..config import Config

def hash_password(password:str)->str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

serializer:URLSafeTimedSerializer|None = None

def get_serializer():
    global serializer
    if serializer is None: serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer

def create_serialized(data:dict,salt:str): return get_serializer().dumps(data, salt=salt)

def try_verify_serialized(token:str,salt:str,max_age:int = 3600):
    error = None
    token_data = None
    try:
        token_data:dict = get_serializer().loads(token,salt=salt,max_age=max_age)
    except SignatureExpired:
        error="el enlace expiro"
    except BadSignature:
        error="token invalido"
    except Exception as e: error = "error desconocido al verificar token"
    
    return error,token_data

def try_verify_daily_serialized(token:str,salt:str):
    return try_verify_serialized(token,salt,86400)
    

def create_serial_token():
    return serializer.dumps

def check_password(password:str,hashed:str)->bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8")
    )