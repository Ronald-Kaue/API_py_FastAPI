from pydantic import BaseModel
from ormbase import ORMBase

class ComentarioBase(BaseModel):
    conteudo: str

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioResponse(ComentarioBase, ORMBase):
    id: int
    mensagem_id: int
