from sqlalchemy.orm import Session
from models import Usuario, Mensagem
from schemas import UsuarioCreate, MensagemCreate
from passlib.hash import bcrypt

def criar_usuario(db: Session, usuario: UsuarioCreate):
    senha_hash = bcrypt.hash(usuario.senha)
    db_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha_hash=senha_hash)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def listar_mensagens(db: Session):
    return db.query(Mensagem).all()

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
