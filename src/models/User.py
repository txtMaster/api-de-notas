from __future__ import annotations
from typing import Optional

from .BaseModel import BaseModel

class User(BaseModel):
    def __init__(
            self,
            id:Optional[int] = None,
            name:Optional[str] = None,
            email:Optional[str] = None,
            password: Optional[str] = None
    ):
        super().__init__(id)
        self.name = name
        self.email = email
        self.password = password
    
    def to_dict(self)->dict:
        return{
            "id":self.id,
            "name":self.name,
            "email":self.email
        }