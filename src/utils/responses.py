from flask import Response, jsonify
from http import HTTPStatus
from src.config import Config

class APIResponse:
    
    @staticmethod
    def CORRECT(code:int,message:str = "ok",payload:dict|list|None = None):
        response = {"message":message}
        if payload is not None: response["payload"] = payload
        return jsonify(response),code
    
    @staticmethod 
    def INCORRECT(code:int,error:str):
        return jsonify({"error":error}),code

    @staticmethod
    def OK(message:str,payload: dict|list|None = None):
        return APIResponse.CORRECT(HTTPStatus.OK,message,payload)
    @staticmethod
    def CREATED(message:str,payload:dict|list|None = None):
        return APIResponse.CORRECT(HTTPStatus.CREATED,message,payload)
    @staticmethod
    def NO_CONTENT(): 
        return Response(status=HTTPStatus.NO_CONTENT)

    @staticmethod
    def BAD_REQUEST(error:str): 
        return APIResponse.INCORRECT(HTTPStatus.BAD_REQUEST,error)
    @staticmethod
    def UNAUTHORIZED(error:str): 
        return APIResponse.INCORRECT(HTTPStatus.UNAUTHORIZED,error)
    @staticmethod
    def FORBIDDEN(error:str): 
        return APIResponse.INCORRECT(HTTPStatus.FORBIDDEN,error)
    @staticmethod
    def NO_FOUND(error:str): 
        return APIResponse.INCORRECT(HTTPStatus.NOT_FOUND,error)
    @staticmethod
    def CONFLICT(error:str): 
        return APIResponse.INCORRECT(HTTPStatus.CONFLICT,error)
    @staticmethod
    def UNPROCESSABLE(error:str): 
        return APIResponse.INCORRECT(HTTPStatus.UNPROCESSABLE_ENTITY,error)
    @staticmethod
    def INTERNAL_ERROR(error:str):
        if Config.DEBUG:
            return APIResponse.INCORRECT(HTTPStatus.INTERNAL_SERVER_ERROR,error)
        else:
            return APIResponse.INCORRECT(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "ocurrio un error, intentelo mas tarde"
            )
    @staticmethod
    def UNAVAILABLE(error:str):
        return APIResponse.INCORRECT(HTTPStatus.SERVICE_UNAVAILABLE,error)