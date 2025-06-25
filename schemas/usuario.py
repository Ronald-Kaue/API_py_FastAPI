from pydantic import BaseModel, EmailStr, validator
from ormbase import ORMBase
import re

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str

    @validator("senha")
    def validar_senha(cls, v):
        if (len(v) < 8 or not re.search(r"\d", v) or not re.search(r"[A-Z]", v)
                or not re.search(r"[a-z]", v) or not re.search(r"[\W_]", v)):
            raise ValueError("A senha deve conter pelo menos 8 caracteres, incluindo maiúscula, minúscula, número e caractere especial.")
        return v

class UsuarioResponse(UsuarioBase, ORMBase):
    id: int
