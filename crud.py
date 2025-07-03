from sqlalchemy.orm import Session
from models.usuario import Usuario
from models.mensagem import Mensagem
from models.comentario import Comentario
from schemas.mensagem import MensagemCreate
from schemas.usuario import UsuarioCreate
from schemas.comentario import ComentarioCreate
from sqlalchemy import select
from security import get_password_hash, verify_password

def criar_usuario(db: Session, usuario: UsuarioCreate):
    senha_hash = get_password_hash(usuario.senha)
    db_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha_hash=senha_hash)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def listar_mensagens(db: Session):
    return db.scalars(select(Mensagem)).all()

def criar_mensagem(db: Session, usuario_id: int, mensagem: MensagemCreate):
    db_mensagem = Mensagem(conteudo=mensagem.conteudo, usuario_id=usuario_id)
    db.add(db_mensagem)
    db.commit()
    db.refresh(db_mensagem)
    return db_mensagem

def get_mensagem(db: Session, id: int):
    return db.query(Mensagem).filter(Mensagem.id == id).first()

def atualizar_mensagem(db: Session, id: int, conteudo: str):
    msg = get_mensagem(db, id)
    if msg:
        msg.conteudo = conteudo
        db.commit()
        db.refresh(msg)
    return msg

def deletar_mensagem(db: Session, id: int):
    msg = get_mensagem(db, id)
    if msg:
        db.delete(msg)
        db.commit()
    return msg

def criar_comentario(db: Session, mensagem_id: int, comentario: ComentarioCreate):
    db_comentario = Comentario(conteudo=comentario.conteudo, mensagem_id=mensagem_id)
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

def criar_comentario_com_user(db: Session, mensagem_id: int, usuario_id: int, comentario: ComentarioCreate):
    db_comentario = Comentario(conteudo=comentario.conteudo, mensagem_id=mensagem_id, autor_id=usuario_id)
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

def listar_comentario(db: Session):
    return db.scalars(select(Comentario)).all()

def get_comentario(db: Session, id: int):
    return db.query(Comentario).filter(Comentario.id == id).first()

def atualizar_comentario(db: Session, id: int, conteudo: str):
    commentary = get_comentario(db, id)
    if commentary:
        commentary.conteudo = conteudo
        db.commit()
        db.refresh(commentary)
    return commentary

def deletar_comentario(db: Session, id: int):
    commentary = get_comentario(db, id)
    if commentary:
        db.delete(commentary)
        db.commit()
    return commentary
