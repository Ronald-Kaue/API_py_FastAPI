from pydantic import BaseModel
import re

class MensagemBase(BaseModel):
    conteudo: str

class MensagemCreate(MensagemBase):
    pass

class MensagemResponse(MensagemBase):
    id: int
    usuario_id: int
    class Config:
        orm_mode = True
