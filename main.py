from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud, schemas
from database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência para obter sessão DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_usuario_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.criar_usuario(db, usuario)

@app.post("/usuarios/{usuario_id}/mensagens", response_model=schemas.MensagemResponse)
def criar_mensagem(usuario_id: int, mensagem: schemas.MensagemCreate, db: Session = Depends(get_db)):
    return crud.criar_mensagem(db, usuario_id, mensagem)

@app.get("/mensagens", response_model=list[schemas.MensagemResponse])
def listar(db: Session = Depends(get_db)):
    return crud.listar_mensagens(db)

@app.get("/mensagens/{id}", response_model=schemas.MensagemResponse)
def get_mensagem(id: int, db: Session = Depends(get_db)):
    msg = crud.get_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg

@app.put("/mensagens/{id}", response_model=schemas.MensagemResponse)
def update_mensagem(id: int, mensagem: schemas.MensagemCreate, db: Session = Depends(get_db)):
    msg = crud.atualizar_mensagem(db, id, mensagem.conteudo)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg

@app.delete("/mensagens/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    msg = crud.deletar_mensagem(db, id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return {"ok": True}
