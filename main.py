from fastapi import FastAPI, Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from security import verify_password
from models.usuario import Usuario
from schemas.usuario import UsuarioResponse, UsuarioCreate
from schemas.mensagem import MensagemResponse, MensagemCreate
from schemas.comentario import ComentarioResponse, ComentarioCreate
from schemas.token import Token, RefreshTokenRequest
from decorators.owner_or_admin_required import owner_or_admin_required
from decorators.comentario_owner_or_admin_required import comentario_owner_or_admin_required
from crud import *
from database import engine, Base, get_db
from security import create_access_token, create_refresh_token, current_user, SECRET_KEY, ALGORITHM

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(Usuario).where(Usuario.email == form_data.username))
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Email ou Senha Inválidos")
    
    access_token = create_access_token(data={'sub': user.email})
    refresh_token = create_refresh_token(data={'sub': user.email})

    return {'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
            }

@app.post("/auth/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    new_access_token = create_access_token(data={"sub": email})
    return {"access_token": new_access_token, "token_type": "Bearer"}


# Usuarios

@app.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_usuario_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return criar_usuario(db, usuario)

# Mensagens

@app.post("/mensagens", response_model=MensagemResponse, status_code=status.HTTP_201_CREATED)
def criar_mensagem_endpoint(mensagem: MensagemCreate, db: Session = Depends(get_db), current_user=Depends(current_user)):
    return criar_mensagem(db, current_user, mensagem)

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
@owner_or_admin_required(get_mensagem_owner_id)
def update_mensagem_endpoint(id: int, mensagem: MensagemCreate, db: Session = Depends(get_db), current_user=Depends(current_user)):
    msg = atualizar_mensagem(db, id, mensagem.titulo, mensagem.conteudo)
    
    return msg

@app.delete("/mensagens/{id}")
@owner_or_admin_required(get_mensagem_owner_id)
def deletar_endpoint(id: int, db: Session = Depends(get_db), current_user=Depends(current_user)):
    deletar_mensagem(db, id)

    return {"INFO": "Mensagem deletada com sucesso"}

# Comentarios

@app.post("/mensagens/{id}/comentarios", response_model=ComentarioResponse)
def criar_comentario_endpoint(id: int, comentario: ComentarioCreate, db: Session = Depends(get_db), current_user=Depends(current_user)):
    return criar_comentario(db, id, current_user, comentario)

@app.get("/comentarios", response_model=list[ComentarioResponse])
def listar(db: Session = Depends(get_db)):
    return listar_comentario(db)

@app.get("/mensagens/{id}/comentarios", response_model=list[ComentarioResponse])
def listar(id: int, db: Session = Depends(get_db)):
    return listar_comentario_by_msg(db, id)

@app.put("/mensagens/{id}/comentarios/{id_comentario}", response_model=ComentarioResponse)
@comentario_owner_or_admin_required(get_comentario_owner_id)
def update_comentario_endpoint(id: int, id_comentario: int, comentario: ComentarioCreate, db: Session = Depends(get_db), current_user=Depends(current_user)):
    msg=get_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    commentary = atualizar_comentario(db, id_comentario, comentario.conteudo)
    
    return commentary

@app.delete("/mensagens/{id}/comentarios/{id_comentario}")
@comentario_owner_or_admin_required(get_comentario_owner_id)
def deletar_endpoint(id: int, id_comentario: int, db: Session = Depends(get_db), current_user=Depends(current_user)):
    msg=get_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    commentary = deletar_comentario(db, id_comentario)
    
    return {"INFO": "Comentário deletada com sucesso"}