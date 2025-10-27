from flask import Blueprint, render_template, request, url_for
from itsdangerous import BadSignature, SignatureExpired

from ..utils.responses import APIResponse
from ..utils.security import create_serialized, get_serializer, try_verify_daily_serialized
from ..utils.routes import verify_body
from ..config import Config
from ..db import mysql

pages_bp = Blueprint("pages",__name__)

@pages_bp.route('/')
def index():
    cursos = ["PHP","JAVA","Python"]
    data = {
       "title":"Index",
       "welcome_message":"!HOLAA!",
       "cursos":cursos,
       "len_cursos":len(cursos)
    ,}
    return render_template("index.html",data=data)

@pages_bp.route("/contact/<name>/<int:age>")
def contact(name,age):
   data={
      "title": "Contacto",
      "name":name,
      "age":age
   }
   return render_template("contact.html",data=data)


@pages_bp.route("/users/verify",methods=["GET"])
def verify_user():
   token = request.args.get("token")
   success=False
   email=None
   error=None
   token_data = None
   if token is None: 
      return render_template("verify.html",data={
         "success":False,
         "error":"Token no proporcionado",
      }),400
   
   error,token_data = try_verify_daily_serialized(token,Config.SALT)

   if token_data is not None:
      email:str = token_data.get("email")
      id:int = int(token_data.get("id"))

   if email is None or id is None: error="error al leer el token"
  
   if error is None:
      try:
         with mysql.connection.cursor() as cur:
            cur.execute("""
                        UPDATE users
                        SET is_verified = TRUE 
                        WHERE id = %s AND email = %s 
                        LIMIT 1
               """,
               (id, email)
            )
            mysql.connection.commit()
            success = cur.rowcount == 1
      except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
      
   return render_template("verify.html",data={
      "success":success,
      "email":email,
      "error":error or "Ocurrió un error o la cuenta ya esta registrada. Intente registrarse con su mismo correo luego de 7 dias",
      "login":Config.LOGIN_URL
   }),200 if success else 400


@pages_bp.route("/recover",methods=["GET"])
def recover_account():
   token = request.args.get("token")
   email = None
   if token is None: 
      return render_template("recover.html",data={
         "success":False,
         "token":token,
         "error":"Token no proporcionado",
      }),400
   
   error,token_data = try_verify_daily_serialized(token,Config.PASS_SALT)
   
   if token_data is not None: email = token_data.get("email")
   else: error="no se pudo leer el token"

   return render_template("recover.html",data={
      "email":email,
      "error":error,
      "token":token,
      "recover_url":url_for("users.recover_password",_external=True)
   }),400 if error else 200