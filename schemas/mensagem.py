from pydantic import BaseModel, ConfigDict


class MensagemBase(BaseModel):
    conteudo: str

class MensagemCreate(MensagemBase):
    pass

class MensagemResponse(MensagemBase):
    id: int
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)
