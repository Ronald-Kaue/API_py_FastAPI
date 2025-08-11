from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ComentarioBase(BaseModel):
    conteudo: str

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioResponse(ComentarioBase):
    id: int
    mensagem_id: int
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)