from __future__ import annotations
from typing import Optional
from src.models.Identificable import Identificable

class BaseModel(Identificable):
    def __init__(self,id:Optional[int]):
        super().__init__(id)

    def to_dict(self)->dict: return {}