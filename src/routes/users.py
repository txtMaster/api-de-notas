from email.message import Message
from flask import Blueprint,jsonify, redirect, render_template, request, url_for
import bcrypt
from itsdangerous import BadSignature, SignatureExpired

from src.config import Config

from src.utils.security import check_password, create_serialized,get_serializer,hash_password, try_verify_daily_serialized
from src.utils.jwt_handler import create_daily_jwt,token_required
from src.utils.responses import APIResponse
from src.utils.routes import verify_body

from src.models.Folder import Folder
from src.models.User import User
from src.models.Note import Note

from src.db import mysql
from src.mail import send_email

from datetime import datetime,timedelta

users_bp = Blueprint("users",__name__)

@users_bp.route("/users/login",methods=["POST"])
@verify_body(required={"email":str,"password":str})
def show_users(data:dict):
  email = data.get("email")
  password = data.get("password")
  if not email or not password: 
    return APIResponse.BAD_REQUEST("password and email no found")

  try: 
    with mysql.connection.cursor() as cur:
      cur.execute("""
                  SELECT 
                    u.is_verified,
                    u.password,
                    u.id as user_id,
                    u.name,
                    u.email,
                    f.id as root_folder_id,
                    f.title as root_folder_title
                  FROM users u INNER JOIN folders f ON f.user_id = u.id AND f.is_root = TRUE
                  WHERE email = %s
      """,(email,))
      results = cur.fetchone()
      if not results: return APIResponse.NO_FOUND("Usuario no econtrado")

      if not results[0]: 
        return APIResponse.UNPROCESSABLE("Verifique su cuenta abriendo el mensaje enviando al correo registrado")
      
      hashed_password = results[1]

      if not check_password(password,hashed_password): 
        return APIResponse.UNAUTHORIZED("Credenciales invalidas")

      user = User(
        id=results[2],
        name=results[3],
        email=results[4],
        password=hashed_password
      )

      token = create_daily_jwt(user.id)

      root_folder = Folder(
        id=results[5],
        title=results[6],
        user_id=user.id,
        is_root=True
      )

      cur.execute("""
                  SELECT id,title 
                  FROM folders 
                  WHERE parent_folder_id = %s ORDER BY title;
      """,(root_folder.id,))

      results = cur.fetchall()

      root_child_folders = []
      for id,title in results:
        root_child_folders.append(Folder(
          id=id,
          title=title
        ).to_dict())


      cur.execute("""
                  SELECT id,title,content
                  FROM notes 
                  WHERE folder_id = %s ORDER BY title;
      """,(root_folder.id,))
      results = cur.fetchall()
      root_folder_notes = []

      for id,title,content in results:
        root_folder_notes.append(Note(
          id=id,
          title=title,
          content=content,
          user_id=user.id
        ).to_dict())
    return APIResponse.OK("usuario validado",{
      "user":user.to_dict(),
      "token":token,
      "root_folder":root_folder.to_dict(),
      "children":{
        "folders":root_child_folders,
        "notes":root_folder_notes
      }
    })
  except Exception as e: return jsonify({"error":str(e)}),500
  

@users_bp.route("/users/register",methods=["POST"])
@verify_body(required={"name":str,"email":str,"password":str})
def register_user(data):
  name = data.get("name")
  email = data.get("email")
  password = data.get("password")
  
  hashedPass = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
  )

  try:
    with mysql.connection.cursor() as cur:
      cur.execute("""
                  SELECT id,is_verified,updated_at FROM users WHERE email = %s LIMIT 1
      """,(email,))
      user = cur.fetchone()

      if user is None:
        root_folder_title = "root"
        cur.execute("""
                    INSERT INTO users (name,email,password,is_verified) 
                    VALUE (%s, %s, %s,FALSE);
        """,(name,email,hashedPass))
        user_id = cur.lastrowid
        cur.execute("""
                    INSERT INTO folders (user_id, parent_folder_id, title, is_root)
                    VALUES (%s, NULL, %s,TRUE);
        """,(user_id,root_folder_title))
        mysql.connection.commit()
      else:
        user_id = user[0]
        is_verified = user[1]
        updated_at = user[2]
        if is_verified: 
          return APIResponse.BAD_REQUEST("la cuenta ya esta registrada correctamente")
        elif datetime.now() - updated_at > timedelta(days=7):
          return APIResponse.BAD_REQUEST("no puede intenter registrar un correo 2 veces seguidas en una misma semana")
        
        cur.execute("""
                    UPDATE users 
                    SET name = %s , password = %s
                    WHERE id = %s AND email = %s;
        """,(name,hashedPass,user_id,email))
        mysql.connection.commit()
        
      user = User(
        id=user_id,
        name=name,
        email=email,
        password=hashedPass
      )

      token = create_serialized({"id":user_id,"email":email},Config.SALT)
      verify_url = url_for("pages.verify_user",token=token, _external = True)

      send_email(
        subject="Verifica tu cuenta", 
        recipients=[email],
        html_body=f"""
        <h3>Confirma tu cuenta</h3>
        <p>Haz click en el siguiente enlace para verificar tu dirección de correo</p>
        <p><a href='{verify_url}'>{verify_url}</a></p>
        <p>Este enlace expira en 1 hora</p>
        """
      )

  except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
  
  return APIResponse.CREATED("Usuario creado, revisa el mensaje de confirmacion enviado al correo registrado para validar tu registro")

@users_bp.route("/users",methods=["DELETE"])
@token_required
def delete_user():
  user_id = request.user_id
  try:
    with mysql.connection.cursor() as cur:
      cur.execute("""DELETE FROM users WHERE id = %s LIMIT 1 """,(user_id,))
      mysql.connection.commit()
      deleted = cur.rowcount == 1
  except Exception as e:return APIResponse.INTERNAL_ERROR(str(e))
  if deleted:return APIResponse.NO_CONTENT()
  else: return APIResponse.BAD_REQUEST("no se encontro el usuario")

@users_bp.route("/users/password",methods=["PATCH"])
@token_required
@verify_body(required={"password":str})
def change_password(data:dict):
  user_id = request.user_id
  password = data.get("password")
  password = hash_password(password)
  try:
    with mysql.connection.cursor() as cur:
      cur.execute("""
                  UPDATE users 
                  SET password = %s
                  WHERE id = %s LIMIT 1 
      """,(password,user_id,))
      mysql.connection.commit()
      deleted = cur.rowcount == 1
  except Exception as e:return APIResponse.INTERNAL_ERROR(str(e))
  if deleted:return APIResponse.NO_CONTENT()
  else: return APIResponse.BAD_REQUEST("no se encontro el usuario")

@users_bp.route("/users/recover",methods=["POST"])
@verify_body(required={"email":str})
def recover_user(data:dict):
  email = data.get("email")
  token = create_serialized({"email":email},Config.PASS_SALT)
  verify_url = url_for("pages.recover_account",token=token,_external=True)
  try:
    send_email(
    subject="Recuperación de cuenta",
    recipients=[email],
    html_body=f"""
      <h3>Recupera tu cuenta</h3>
      <p>Haz click en el siguiente enlace para cambiar la contraseña de tu cuenta</p>
      <p><a href='{verify_url}'>{verify_url}</a></p>
      <p>Este enlace expira en 1 hora</p>
    """
    )
  except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
  return APIResponse.OK("Se envio un mensaje al correo registrado junto a un enlace para recuperar su cuenta")

@users_bp.route("/users/recover-password",methods=["PATCH"])
@verify_body(required={"token":str,"password":str})
def recover_password(data:dict):
  token = data.get("token")
  password = data.get("password")

  error,token_data = try_verify_daily_serialized(token,Config.PASS_SALT)
  password = hash_password(password)
  email = token_data.get("email")

  if error is None and email is not None:
    try:
      with mysql.connection.cursor() as cur:
        cur.execute("""
                    UPDATE users
                    SET password = %s
                    WHERE email = %s AND TIMESTAMPDIFF(HOUR, updated_at,NOW()) >= 24
                    LIMIT 1
        """,(password,email))
        mysql.connection.commit()
        if cur.rowcount == 0: 
          return APIResponse.BAD_REQUEST("no se encontro el usuario o ya se actualizo recientemente, intentelo luego de 24 horas")
        
    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
    return APIResponse.NO_CONTENT()
  else: return APIResponse.INTERNAL_ERROR(error=error or "email no reconocido")