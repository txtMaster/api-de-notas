from flask import Blueprint, jsonify, request

from ..models.Folder import Folder
from ..models.Note import Note

from ..db import mysql
from ..utils.jwt_handler import token_required
from ..utils.responses import APIResponse

folders_bp = Blueprint("folders",__name__)

@folders_bp.route("/folders/<int:folder_id>/get_childs",methods=["GET"])
@token_required
def get_childs(folder_id:int):
    if not folder_id: return APIResponse.BAD_REQUEST("folder_id required")
    user_id = request.user_id

    try:
        with mysql.connection.cursor() as cur:
            
            cur.execute("""
                        SELECT id FROM folders
                        WHERE id = %s AND user_id = %s
            """,(folder_id,user_id))
            folder_checked = cur.fetchone()
            if not folder_checked: 
                return APIResponse.NO_FOUND("Folder no encontrado")
            
            cur.execute("""
                        SELECT id,title,created_at
                        FROM folders
                        WHERE parent_folder_id = %s AND user_id = %s
            """,(folder_id,user_id))                        
            results = cur.fetchall()
            folders = []
            for id,title,created_at in results:
                folders.append(Folder(
                    id=id,
                    title=title,
                    created_at=created_at,
                    is_root=False
                ).to_dict())

            cur.execute("""
                        SELECT id,title,content,created_at,updated_at
                        FROM notes
                        WHERE folder_id = %s AND user_id = %s
            """,(folder_id,user_id))
            results = cur.fetchall()

        notes = []
        for id,title,content,created_at,updated_at in results:
            notes.append(Note(
                id=id,
                title=title,
                content=content,
                created_at=created_at,
                updated_at=updated_at
            ).to_dict())

        return jsonify({
            "message":"ok",
            "payload":{
                "folders":folders,
                "notes":notes,
            }
        })

    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))

    