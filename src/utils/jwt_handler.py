from functools import wraps
from flask import jsonify, request
import jwt
import datetime

from ...src.config import Config

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = "HS256"

def create_jwt(user_id:int,expire_in:int = 3600)->str:
    payload = {
        "user_id":user_id,
        "exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_in),
        "iat":datetime.datetime.utcnow()
    }
    return jwt.encode(payload,SECRET_KEY,algorithm="HS256")

def decode_jwt(token:str)->dict:
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("token invalido")

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer"): 
            return jsonify({"error":"token required"}),401

        token = auth.split(" ")[1]

        try:
            decoded = decode_jwt(token)
            request.user_id = decoded["user_id"]
        except ValueError as e:
            return jsonify({"error":str(e)}),401
        
        return f(*args,**kwargs)
    return decorated

def create_daily_jwt(user_id:int):
    return create_jwt(user_id,86400)