from flask import Blueprint, request

from ..utils.routes import verify_body

from ..utils.responses import APIResponse
from ..db import mysql

from ..utils.jwt_handler import token_required

from ..models.Note import Note

notes_bp = Blueprint("notes",__name__)

@notes_bp.route("/notes/create",methods=["POST"])
@token_required
@verify_body(required={"title":str,"content":str,"folder_id":int})
def create_note(data:dict):
    user_id = request.user_id
    title = data["title"]
    content = data["content"]
    folder_id = data["folder_id"]

    try:
        with mysql.connection.cursor() as cur:
            cur.execute("""
                        SELECT folder_id FROM notes
                        WHERE user_id = %s
            """,(user_id,))

            if not cur.fetchone(): 
                return APIResponse.BAD_REQUEST("Carpeta no encontrada")

            
            cur.execute("""
                        INSERT INTO notes (title,content,user_id,folder_id)
                        VALUES (%s,%s,%s,%s)
            """,(title,content,user_id,folder_id))

            note_id = cur.lastrowid
            mysql.connection.commit()

            return APIResponse.CREATED("nota creada",{"note_id":note_id})
    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
    
    