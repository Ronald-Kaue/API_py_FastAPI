from fastapi import FastAPI, Depends, HTTPException
from http import HTTPStatus
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from security import verify_password
from models.usuario import Usuario
from schemas.usuario import UsuarioResponse, UsuarioCreate
from schemas.mensagem import MensagemResponse, MensagemCreate
from schemas.comentario import ComentarioResponse, ComentarioCreate
from schemas.token import Token
from crud import *
from database import engine, Base, get_db
from security import create_access_token, current_user

app = FastAPI()

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(Usuario).where(Usuario.email == form_data.username))
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Email ou Senha Inválidos")
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}

# Usuarios

@app.post("/usuarios", response_model=UsuarioResponse)
def criar_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_usuario_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return criar_usuario(db, usuario)

# Mensagens

@app.post("/usuarios/{usuario_id}/mensagens", response_model=MensagemResponse)
def criar_mensagem_endpoint(usuario_id: int, mensagem: MensagemCreate, db: Session = Depends(get_db), current_user=Depends(current_user)):
    if current_user.id != usuario_id and current_user.role != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions'
        )
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
def update_mensagem_endpoint(id: int, mensagem: MensagemCreate, db: Session = Depends(get_db), current_user=Depends(current_user)):
    mensagem_var = get_mensagem(db, id)
    if current_user.id != mensagem_var.usuario_id and current_user.role != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions'
        )
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    msg = atualizar_mensagem(db, current_user.id, mensagem.conteudo)
    
    return msg

@app.delete("/mensagens/{id}")
def deletar_endpoint(id: int, db: Session = Depends(get_db), current_user=Depends(current_user)):
    mensagem_var = get_mensagem(db, id)
    if not mensagem_var:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    if current_user.id != mensagem_var.usuario_id and current_user.role != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions'
        )
    deletar_mensagem(db, id)
    return {"INFO": "Mensagem deletada com sucesso"}

# Comentarios

@app.post("/mensagens/{mensagem_id}/comentarios", response_model=ComentarioResponse)
def criar_comentario_endpoint(mensagem_id: int, comentario: ComentarioCreate, db: Session = Depends(get_db)):
    return criar_comentario(db, mensagem_id, comentario)

@app.post("/usuario/{usuario_id}/mensagens/{mensagem_id}/comentarios", response_model=ComentarioResponse)
def criar_comentario_with_user_endpoint(usuario_id:int, mensagem_id: int, comentario: ComentarioCreate, db: Session = Depends(get_db), current_user=Depends(current_user)):
    if current_user.id != usuario_id and current_user.role != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions'
        )
    return criar_comentario_com_user(db, mensagem_id, current_user.id, comentario)

@app.get("/comentarios", response_model=list[ComentarioResponse])
def listar(db: Session = Depends(get_db)):
    return listar_comentario(db)

@app.put("/comentarios/{id}", response_model=ComentarioResponse) 
def update_comentario_endpoint(id: int, comentario: ComentarioCreate, db: Session = Depends(get_db), current_user=Depends(current_user)):
    comentario_var = get_comentario(db, id)
    if current_user.id != comentario_var.usuario_id and current_user.role != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions'
        )
    
    if not get_comentario(id=id):
        raise HTTPException(status_code=404, detail="Comentário não encontrada")
    
    commentary = atualizar_comentario(db, id, comentario.conteudo)
        
    return commentary

@app.delete("/comentarios/{id}")
def deletar_endpoint(id: int, db: Session = Depends(get_db), current_user=Depends(current_user)):
    comentario = get_comentario(db, id)
    if current_user.id != comentario.usuario_id and current_user.role != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions'
        )
    
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrada")
    
    commentary = deletar_comentario(db, id)
        
    return commentary