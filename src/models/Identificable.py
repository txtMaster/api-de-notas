from typing import Optional


class Identificable:
    id: Optional[int]
    def __init__(self,id:Optional[int]):
        self.id = id