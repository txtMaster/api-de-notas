from flask import Blueprint, render_template, request
from itsdangerous import BadSignature, SignatureExpired

from src.utils.responses import APIResponse

from src.utils.security import get_serializer

from src.config import Config
from src.db import mysql

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
   print("-------------------------------------------")
   token = request.args.get("token")
   success=False
   email=None
   expired=False
   error=None
   token_data = None
   if token is None: 
      error="token requerido"
   try:
      token_data = get_serializer().loads(token,salt=Config.SALT,max_age=3600)
   except SignatureExpired:
      error="el enlace expiro"
      expired = True
   except BadSignature:
      error="token invalido"
   except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
   print(token_data or "NO HAY TOKEN")

   if token_data is not None:
      email:str = token_data.get("email")
      id:int = int(token_data.get("id"))

   if email is None or id is None: 
      error="error al leer el token"
      expired=True
  
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
      except Exception as e: 
         return APIResponse.INTERNAL_ERROR(str(e))
      
   return render_template("verify.html",data={
      "success":success,
      "email":email,
      "error":error or "Ocurrió un error o la cuenta ya esta registrada. Intente registrarse con su mismo correo luego de 7 dias",
      "login":Config.LOGIN_URL,
      "expired":expired
   }),200 if success else 400