from __future__ import annotations
from typing import Optional
from datetime import date, datetime

from .BaseModel import BaseModel

class Folder(BaseModel):
    def __init__(
            self,
            id:Optional[int] = None,
            title:Optional[str] = None,
            user_id:Optional[int] = None,
            parent_folder_id:Optional[int] = None,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None,
            is_root:bool = False
    ):
        super().__init__(id)
        self.title = title
        self.user_id = user_id
        self.parent_folder_id = parent_folder_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_root = is_root
    
    def to_dict(self)->dict:
        return{
            "id":self.id,
            "title":self.title,
            "user_id":self.user_id,
            "parent_folder_id":self.parent_folder_id,
            "created_at":self.created_at.isoformat() if self.created_at is not None else None,
            "updated_at":self.updated_at.isoformat() if self.updated_at is not None else None,
            "is_root":self.is_root
        }