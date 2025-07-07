from pydantic import BaseModel, ConfigDict


class ComentarioBase(BaseModel):
    conteudo: str

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioResponse(ComentarioBase):
    id: int
    mensagem_id: int

    model_config = ConfigDict(from_attributes=True)