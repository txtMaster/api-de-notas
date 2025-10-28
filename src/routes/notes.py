from datetime import datetime, timezone
from typing import Optional
from flask import Blueprint, request

from ..utils.routes import verify_body
from ..utils.responses import APIResponse
from ..db import mysql
from ..utils.jwt_handler import token_required
from ..models.Note import Note

notes_bp = Blueprint("notes",__name__)

@notes_bp.route("/notes",methods=["POST"])
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
                        SELECT id FROM folders
                        WHERE user_id = %s AND id = %s
            """,(user_id,folder_id))

            if cur.fetchone() is None: 
                return APIResponse.BAD_REQUEST("Carpeta no encontrada")

            
            cur.execute("""
                        INSERT INTO notes (title,content,user_id,folder_id)
                        VALUES (%s,%s,%s,%s)
                        RETURNING id,created_at
            """,(title,content,user_id,folder_id))

            note = cur.fetchone()
            mysql.connection.commit()
            if note is None: return APIResponse.BAD_REQUEST("no se creo la nota")
        note = Note(id=note[0],created_at=note[1])
    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
    return APIResponse.CREATED("nota creada",{"note":note.to_dict()})
    

@notes_bp.route("/notes/<int:note_id>",methods=["PATCH"])
@token_required
@verify_body(optional={"title":str,"content":str})
def update_note(note_id,data:dict):
    user_id = request.user_id
    title = data.get("title")
    content = data.get("content")
    updated_at:Optional[datetime] = None
    set_query_section:dict = {
        "query":[],
        "params":[]
    }
    
    if title is not None: 
        set_query_section["query"].append("title = %s")
        set_query_section["params"].append(title)
    if content is not None: 
        set_query_section["query"].append("content = %s")
        set_query_section["params"].append(content)

    if len(set_query_section["params"]) == 0: 
        return APIResponse.BAD_REQUEST("se requiere minimo un valor para actualizar")

    set_query_str = ", ".join(set_query_section["query"])
    
    try:
        with mysql.connection.cursor() as cur:
            updated_at = datetime.now(timezone.utc)
            cur.execute(f"""
                        UPDATE notes
                        SET {set_query_str} AND updated_at = %s
                        WHERE id = %s AND user_id = %s
                        LIMIT 1
            """,(tuple(set_query_section["params"]) + (updated_at,note_id,user_id,)))

            mysql.connection.commit()
            
            if cur.rowcount == 0: 
                return APIResponse.NO_FOUND("No se encontro la nota o hubo cambios")

    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))

    return APIResponse.OK("nota actualiada",{"updated_at":updated_at.isoformat()})
    

@notes_bp.route("/notes",methods=["DELETE"])
@token_required
@verify_body(required={"note_ids":list})
def delete_notes(data:dict):
    user_id = request.user_id
    note_ids = data["note_ids"]
    notes_len = len(note_ids)

    if notes_len == 0 or not all(isinstance(v,int) for v in note_ids):
        return APIResponse.BAD_REQUEST("note_ids debe ser una lista no vacia de ints")
    
    if notes_len > 1:
        where_query = f"id IN({','.join(['%s'] * notes_len)})"
    else:
        where_query = "id = %s"
    
    try:
        with mysql.connection.cursor() as cur:
            cur.execute(f"""
                        DELETE FROM notes 
                        WHERE {where_query} AND user_id = %s
            """,(*note_ids,user_id))

            if cur.rowcount != len(note_ids): 
                return APIResponse.NO_FOUND("no se pudo borrar todas las notas")
            
            mysql.connection.commit()
            
            
    except Exception as e: APIResponse.INTERNAL_ERROR(str(e))
    return APIResponse.NO_CONTENT()


@notes_bp.route("/notes/move",methods=["PATCH"])
@token_required
@verify_body(required={"folder_id":int,"note_ids":list})
def move_note(data:dict):
    update_at: Optional[datetime] = None
    user_id = request.user_id
    folder_id:int = int(data.get("folder_id"))
    note_ids:list = data.get("note_ids")

    if(
        len(note_ids) == 0 or 
        not all(isinstance(v,int) for v in note_ids)
    ): 
        return APIResponse.BAD_REQUEST("note_ids debe ser una lista no vacia de enteros")
    
    if len(note_ids) > 1:
        in_func_query = f"id IN({','.join(['%s'] * len(note_ids))})"
    else:
        in_func_query = "id = %s "
    
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("""
                        SELECT id 
                        FROM folders 
                        WHERE id = %s AND user_id = %s LIMIT 1
            """,(folder_id,user_id))

            if cur.fetchone() is None: 
                return APIResponse.BAD_REQUEST("folder no encontrado")
            
            update_at = datetime.now(timezone.utc)
            cur.execute(f"""
                        UPDATE notes 
                        SET folder_id = %s, updated_at = %s
                        WHERE {in_func_query} AND user_id = %s
            """,(folder_id,update_at,*note_ids,user_id))
            mysql.connection.commit()

            if cur.rowcount == 0: 
                return APIResponse.NO_FOUND("no se encontro alguna nota")
            
    except Exception as e: APIResponse.INTERNAL_ERROR(str(e))
    return APIResponse.OK("notas movidas correctamente",{
        "updated_at":update_at.isoformat()
    })