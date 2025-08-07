from sqlalchemy.orm import Session
from models.usuario import Usuario
from models.mensagem import Mensagem
from models.comentario import Comentario
from schemas.mensagem import MensagemCreate
from schemas.usuario import UsuarioCreate
from schemas.comentario import ComentarioCreate
from fastapi import HTTPException
from sqlalchemy import select
from security import get_password_hash

def criar_usuario(db: Session, usuario: UsuarioCreate):
    if usuario.senha == "" or None and usuario.email == "" or None and usuario.nome == "" or None:
        senha_hash = get_password_hash(usuario.senha)
        db_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha_hash=senha_hash, role = usuario.role)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    else:
        return {"errors": {"email": ["Campo obrigatório."], "senha": ["Campo obrigatório."]}}

# CRUDs mensagens

def get_usuario(db: Session, id: str):
    return db.query(Usuario).filter(Usuario.id == id).first()

def get_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def listar_mensagens(db: Session):
    return db.scalars(select(Mensagem)).all()

def criar_mensagem(db: Session, current_user, mensagem: MensagemCreate):
    db_mensagem = Mensagem(titulo=mensagem.titulo, conteudo=mensagem.conteudo, usuario_id=current_user.id)
    db.add(db_mensagem)
    db.commit()
    db.refresh(db_mensagem)
    return db_mensagem

def get_mensagem(db: Session, id: int):
    return db.query(Mensagem).filter(Mensagem.id == id).first()

# Decorators mensagens

def get_mensagem_owner_id(db, id):
    mensagem = get_mensagem(db, id)
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return mensagem.usuario_id

# CRUDs mensagens again
def atualizar_mensagem(db: Session, id: int, titulo: str, conteudo: str):
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    
    msg = get_mensagem(db, id)
    if msg.titulo:
        msg.titulo = titulo
        db.commit()
        db.refresh(msg)
    
    if msg.conteudo:
        msg.conteudo = conteudo
        db.commit()
        db.refresh(msg)
    else:
        return {"errors": {"conteudo": ["Campo obrigatório."]}}
    
    return msg

def deletar_mensagem(db: Session, id: int):
    msg = get_mensagem(db, id)
    if msg:
        db.delete(msg)
        db.commit()
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg

# CRUDs comentarios

def criar_comentario(db: Session, id: int, current_user, comentario: ComentarioCreate):
    msg = get_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    
    db_comentario = Comentario(conteudo=comentario.conteudo, mensagem_id=id, autor_id=current_user.id)
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

def listar_comentario(db: Session):
    return db.scalars(select(Comentario)).all()

def listar_comentario_by_msg(db: Session, id: int):
    return db.query(Comentario).filter(Comentario.mensagem_id == id).all()

def get_comentario(db: Session, id: int):
    return db.query(Comentario).filter(Comentario.id == id).first()

# Decorators comentarios

def get_comentario_owner_id(db: Session, id_comentario: int):
    comentario = get_comentario(db, id_comentario)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    return comentario.autor_id

# CRUDs comentarios again

def atualizar_comentario(db: Session, id: int, conteudo: str):
    commentary = get_comentario(db, id)
    if commentary:
        commentary.conteudo = conteudo
        db.commit()
        db.refresh(commentary)
    if not get_comentario(db, id):
        raise HTTPException(status_code=404, detail="Comentário não encontrada")
    return commentary

def deletar_comentario(db: Session, id: int):
    commentary = get_comentario(db, id)
    if commentary:
        db.delete(commentary)
        db.commit()
    if not commentary:
        raise HTTPException(status_code=404, detail="Comentário não encontrada")

    return commentary
