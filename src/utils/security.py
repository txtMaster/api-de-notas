import bcrypt
from itsdangerous import URLSafeTimedSerializer

from ...src.config import Config

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

def create_serial_token():
    return serializer.dumps

def check_password(password:str,hashed:str)->bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8")
    )