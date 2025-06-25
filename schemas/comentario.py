from pydantic import BaseModel
import re

class ComentarioBase(BaseModel):
    conteudo: str

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioResponse(ComentarioBase):
    id: int
    usuario_id: int
    class Config:
        orm_mode = True
