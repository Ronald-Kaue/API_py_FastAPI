from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioResponse, UsuarioCreate
from schemas.mensagem import MensagemResponse, MensagemCreate
from schemas.comentario import ComentarioResponse, ComentarioCreate
from schemas.token import Token
from crud import *
from database import engine, Base, get_db
from security import create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = Session.scalar(select(Usuario).where(Usuario.email == form_data.username))
    if not user or not verify_password(form_data, Usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Email ou Senha Inválidos")
    access_token = create_access_token(data={'sub': Usuario.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}

@app.post("/usuarios", response_model=UsuarioResponse)
def criar_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_usuario_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return criar_usuario(db, usuario)

@app.post("/usuarios/{usuario_id}/mensagens", response_model=MensagemResponse)
def criar_mensagem_endpoint(usuario_id: int, mensagem: MensagemCreate, db: Session = Depends(get_db)):
    return criar_mensagem(db, usuario_id, mensagem)

@app.get("/mensagens", response_model=list[MensagemResponse])
def listar(db: Session = Depends(get_db)):
    return listar_mensagens(db)

@app.get("/mensagens/{id}", response_model=MensagemResponse)
def get_mensagem_endpoint(id: int, db: Session = Depends(get_db)):
    msg = get_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg

@app.put("/mensagens/{id}", response_model=MensagemResponse)
def update_mensagem_endpoint(id: int, mensagem: MensagemCreate, db: Session = Depends(get_db)):
    msg = atualizar_mensagem(db, id, mensagem.conteudo)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg

@app.delete("/mensagens/{id}")
def deletar_endpoint(id: int, db: Session = Depends(get_db)):
    msg = deletar_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return {"INFO": "Mensagem deletada com sucesso"}

@app.post("/mensagens/{mensagem_id}/comentarios", response_model=ComentarioResponse)
def criar_comentario_endpoint(mensagem_id: int, comentario: ComentarioCreate, db: Session = Depends(get_db)):
    return criar_comentario(db, mensagem_id, comentario)

@app.post("/usuario/{usuario_id}/mensagens/{mensagem_id}/comentarios", response_model=ComentarioResponse)
def criar_comentario_with_user_endpoint(usuario_id:int, mensagem_id: int, comentario: ComentarioCreate, db: Session = Depends(get_db)):
    return criar_comentario_com_user(db, mensagem_id, usuario_id, comentario)

@app.get("/comentarios", response_model=list[ComentarioResponse])
def listar(db: Session = Depends(get_db)):
    return listar_comentario(db)

@app.put("/comentarios/{id}", response_model=ComentarioResponse)
def update_comentario_endpoint(id: int, comentario: ComentarioCreate, db: Session = Depends(get_db)):
    commentary = atualizar_comentario(db, id, comentario.conteudo)
    if not commentary:
        raise HTTPException(status_code=404, detail="Comentário não encontrada")
    return commentary

@app.delete("/comentarios/{id}")
def deletar_endpoint(id: int, db: Session = Depends(get_db)):
    commentary = deletar_comentario(db, id)
    if not commentary:
        raise HTTPException(status_code=404, detail="Comentário não encontrada")
    return {"INFO": "Comentário deletada com sucesso"}