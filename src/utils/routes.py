from functools import wraps

from flask import jsonify, request
from http import HTTPStatus


def verify_body(required:dict = None , optional:dict=None):
    """decorador para validar el contenido del body de un solicitud"""

    required = required or {}
    optional = optional or {}
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            data = request.get_json(silent=True) or {}
            validated_data = {}
            errors = {}
            for field,expected_type in required.items():
                value = data.get(field)
                if value is None or not isinstance(value, expected_type):
                    errors[field] = f"Required expected {expected_type.__name__} got {type(value).__name__}"

            for field,expected_type in optional.items():
                if field in data and not isinstance(data[field],expected_type):
                    errors[field] = f"Expected {expected_type.__name__} got {type(data[field]).__name__}"
            
            if errors: 
                return jsonify({"error":"Invalid body","payload":errors}),HTTPStatus.BAD_REQUEST
            
            validated_data = {
                **{k:data.get(k) for k in required},
                **{k:data.get(k) for k in optional if k in data}    
            }

            return f(*args, data=validated_data,**kwargs)
        return wrapper    
    return decorator