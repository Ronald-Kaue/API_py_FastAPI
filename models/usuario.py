from sqlalchemy import Column, Integer, String, func, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from zoneinfo import ZoneInfo
from datetime import datetime
from database import Base
from pydantic import ConfigDict

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default = "user")
    data_criacao = Column(DateTime, default=func.now())
    
    mensagens = relationship("Mensagem", back_populates="autor")
    comentario = relationship("Comentario", back_populates="autor")

    model_config = ConfigDict(from_attributes=True)