from typing import Optional
from flask import Blueprint,jsonify, request
import bcrypt

from ..utils.security import check_password
from ..utils.jwt_handler import create_daily_jwt
from ..utils.responses import APIResponse
from ..utils.routes import verify_body

from ..models.Folder import Folder
from ..models.User import User
from ..models.Note import Note
from ..db import mysql

users_bp = Blueprint("users",__name__)

@users_bp.route("/users/login",methods=["POST"])
def show_users():
  data:dict = request.json or {}
  email = data.get("email")
  password = data.get("password")
  if not email or not password: 
    return APIResponse.BAD_REQUEST("password and email no found")

  try: 
    with mysql.connection.cursor() as cur:
      cur.execute("""
                  SELECT 
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
      
      hashed_password = results[0]

      if not check_password(password,hashed_password): 
        return APIResponse.UNAUTHORIZED("Credenciales invalidas")

      user = User(
        id=results[1],
        name=results[2],
        email=results[3],
        password=hashed_password
      )

      token = create_daily_jwt(user.id)

      root_folder = Folder(
        id=results[4],
        title=results[5],
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
                  INSERT INTO users (name,email,password) 
                  VALUE (%s, %s, %s);
      """,(name,email,hashedPass))
      user_id = cur.lastrowid
      mysql.connection.commit()

      user = User(
        id=user_id,
        name=name,
        email=email,
        password=hashedPass
      )
      root_folder_title = "root"
      cur.execute("""
                  INSERT INTO folders (user_id, parent_folder_id, title, is_root)
                  VALUES (%s, NULL, %s,TRUE);
      """,(user.id,root_folder_title))
      root_folder_id = cur.lastrowid
      mysql.connection.commit()

      cur.execute("""
                  SELECT created_at FROM folders WHERE id = %s;
      """,(root_folder_id,))
      
      folder_created_at = cur.fetchone()[0]

      root_folder = Folder(
        id=root_folder_id,
        title=root_folder_title,
        is_root=True,
        user_id=user.id,
        parent_folder_id=None,
        created_at= folder_created_at
      )
    return APIResponse.CREATED("user created",{
      "user":user.to_dict(),
      "root_folder":root_folder.to_dict()
    })

  except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))