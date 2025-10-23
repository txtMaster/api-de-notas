from __future__ import annotations
from typing import Optional
from datetime import date

from .BaseModel import BaseModel

class Note(BaseModel):
    def __init__(
            self,
            id:Optional[int] = None,
            title:Optional[str] = None,
            content:Optional[int] = None,
            user_id:Optional[int] = None,
            folder_id:Optional[int] = None,
            created_at: Optional[date] = None,
            updated_at: Optional[date] = None
    ):
        super().__init__(id)
        self.title = title
        self.content = content
        self.user_id = user_id
        self.folder_id = folder_id
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self)->dict:
        return{
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "user_id":self.user_id,
            "parent_folder_id":self.folder_id,
            "created_at":self.created_at,
            "updated_at":self.updated_at,
        }