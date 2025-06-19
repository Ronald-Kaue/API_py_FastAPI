from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String, nullable=False)
    
    mensagens = relationship("Mensagem", back_populates="autor")

class Mensagem(Base):
    __tablename__ = "mensagens"
    
    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    autor = relationship("Usuario", back_populates="mensagens")
