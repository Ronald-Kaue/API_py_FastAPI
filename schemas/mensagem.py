from pydantic import BaseModel
from ormbase import ORMBase

class MensagemBase(BaseModel):
    conteudo: str

class MensagemCreate(MensagemBase):
    pass

class MensagemResponse(MensagemBase, ORMBase):
    id: int
    usuario_id: int
