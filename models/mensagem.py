from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import ConfigDict

class Mensagem(Base):
    __tablename__ = "mensagens"
    
    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    autor = relationship("Usuario", back_populates="mensagens")
    comentario = relationship("Comentario", back_populates="mensagens", cascade="all, delete-orphan")

    model_config = ConfigDict(from_attributes=True)