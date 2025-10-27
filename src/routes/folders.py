from flask import Blueprint, jsonify, request

from ..models.Folder import Folder
from ..models.Note import Note
from ..db import mysql
from ..utils.jwt_handler import token_required
from ..utils.responses import APIResponse
from ..utils.routes import verify_body

folders_bp = Blueprint("folders",__name__)

@folders_bp.route("/folders/<int:folder_id>/childs",methods=["GET"])
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

        return APIResponse.OK("contenido encontrado",{
            "folders":folders,
            "notes":notes,
        })

    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))


@folders_bp.route("/folders",methods=["POST"])
@token_required
@verify_body(required={"parent_folder_id":int,"title":str})
def create_folder(data:dict):
    parent_folder_id = data["parent_folder_id"]
    title = data["title"]
    user_id = request.user_id

    try:
        with mysql.connection.cursor() as cur:    
            cur.execute("""
                        INSERT INTO folders (user_id,title,parent_folder_id)
                        VALUES (%s,%s,%s)
                        RETURNING id, created_at
            """,(user_id,title,parent_folder_id))
            folder = cur.fetchone()
            mysql.connection.commit()
            if folder is None: return APIResponse.BAD_REQUEST("folder no creado")
        folder = Folder(id=folder[0],created_at=folder[1])
    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
    return APIResponse.CREATED("folder creado",{
        "folder" : folder.to_dict()
    })

@folders_bp.route("/folders/move",methods=["PATCH"])
@token_required
@verify_body(required={"parent_folder_id":int,"folder_ids":list})
def move_folder(data:dict):

    folder_ids:list = data["folder_ids"]
    parent_folder_id:int = data["parent_folder_id"]
    user_id = request.user_id

    if(
        len(folder_ids) == 0 or 
        not all(isinstance(x,int) for x in folder_ids)
    ): 
        return APIResponse.BAD_REQUEST("folder_ids debe ser una lista no vacia de enteros")

    if parent_folder_id in folder_ids: 
        return APIResponse.BAD_REQUEST("no se puede asignar un folder como su propio folde contenedor")

    if len(folder_ids) > 1:
        in_func_query = f"IN({','.join(['%s'] * len(folder_ids))})"
    else:
        in_func_query = " = %s "

    params = (parent_folder_id,) + tuple(folder_ids) + (user_id,)

    try:
        with mysql.connection.cursor() as cur:    

            cur.execute("""
                        SELECT id FROM folders WHERE user_id = %s AND id = %s
            """,(user_id,parent_folder_id))
            if cur.fetchone() is None: 
                return APIResponse.NO_FOUND("nuevo folder padre no encontrado")

            cur.execute(f"""
                        UPDATE folders
                        SET parent_folder_id = %s
                        WHERE id {in_func_query} AND user_id = %s
            """,params)
            mysql.connection.commit()

            if cur.rowcount == 0: 
                return APIResponse.BAD_REQUEST("no se pudo mover los folders")

    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
    return APIResponse.OK("folders movido")

    


@folders_bp.route("/folders/<int:folder_id>/rename",methods=["PATCH"])
@token_required
@verify_body(required={"title":str})
def rename_folder(folder_id:int,data:dict):
    title = data["title"]
    user_id = request.user_id

    try:
        with mysql.connection.cursor() as cur:    
            cur.execute("""
                        UPDATE folders
                        SET title = %s
                        WHERE id = %s AND user_id = %s
                        LIMIT 1
            """,(title,folder_id,user_id))
            mysql.connection.commit()

            if cur.rowcount == 0:
                return APIResponse.BAD_REQUEST("folder no renombrado")
            
    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
    return APIResponse.NO_CONTENT()

@folders_bp.route("/folders",methods=["DELETE"])
@token_required
@verify_body(required={"folder_ids":list})
def delete_folders(data:dict):
    user_id = request.user_id
    folders_ids = data["folder_ids"]
    if not all(isinstance(id,int) for id in folders_ids) or len(folders_ids) == 0:
        return APIResponse.BAD_REQUEST("folders_ids debe ser una lista no vacia de ids de folders a borrar")

    len_folders = len(folders_ids)
    if len_folders > 1:
        where_query = f"id IN({', '.join(['%s'] * len_folders)})"
    else:
        where_query = "id = %s"
    

    try:
        with mysql.connection.cursor() as cur:    
            cur.execute(f"""
                        DELETE from folders
                        WHERE {where_query} AND user_id = %s
            """,(*folders_ids,user_id))

            if cur.rowcount != len(folders_ids):
                return APIResponse.BAD_REQUEST("no se pudieron borrar los folders")
            
            mysql.connection.commit()
            
    except Exception as e: return APIResponse.INTERNAL_ERROR(str(e))
    return APIResponse.NO_CONTENT()