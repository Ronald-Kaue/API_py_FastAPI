from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioResponse, UsuarioCreate
from schemas.mensagem import MensagemResponse, MensagemCreate
from schemas.comentario import ComentarioResponse, ComentarioCreate
from crud import criar_usuario, get_usuario_por_email, listar_mensagens, criar_mensagem, get_mensagem, atualizar_mensagem, deletar_mensagem, criar_comentario
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/usuarios", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_usuario_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return criar_usuario(db, usuario)

@app.post("/usuarios/{usuario_id}/mensagens", response_model=MensagemResponse)
def criar_mensagem(usuario_id: int, mensagem: MensagemCreate, db: Session = Depends(get_db)):
    return criar_mensagem(db, usuario_id, mensagem)

@app.get("/mensagens", response_model=list[MensagemResponse])
def listar(db: Session = Depends(get_db)):
    return listar_mensagens(db)

@app.get("/mensagens/{id}", response_model=MensagemResponse)
def get_mensagem(id: int, db: Session = Depends(get_db)):
    msg = get_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg

@app.put("/mensagens/{id}", response_model=MensagemResponse)
def update_mensagem(id: int, mensagem: MensagemCreate, db: Session = Depends(get_db)):
    msg = atualizar_mensagem(db, id, mensagem.conteudo)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg

@app.delete("/mensagens/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    msg = deletar_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return {"INFO": "Mensagem deletada com sucesso"}

@app.post("/mensagens/{mensagem_id}/comentarios", response_model=MensagemResponse)
def criar_comentario(mensagem_id: int, comentario: ComentarioCreate, db: Session = Depends(get_db)):
    return criar_comentario(db, mensagem_id, comentario)
