from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Comentario(Base):
    __tablename__ = "comentarios"
    
    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(String, nullable=False)
    mensagem_id = Column(Integer, ForeignKey("mensagens.id"))
    autor_id = Column(Integer, ForeignKey("usuarios.id"))
    publicado_em = Column(DateTime, default=func.now())

    autor = relationship("Usuario", back_populates="comentario")
    mensagens = relationship("Mensagem", back_populates="comentario")