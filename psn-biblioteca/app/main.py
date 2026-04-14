from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from bson.objectid import ObjectId
from pathlib import Path

from app.models.jogo import JogoBase, JogoResponse
from app.database.mongodb import mongodb

app = FastAPI(
    title="🎮 Biblioteca PlayStation",
    description="API para gerenciamento de jogos - PS4 e PS5",
    version="1.0.0"

)

static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def pagina_principal():
    html_file = Path(__file__).parent / "static" / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    raise HTTPException(status_code=404, detail="HTML não encontrado")

@app.post("/jogos/", response_model=JogoResponse, status_code=status.HTTP_201_CREATED)
async def adicionar_jogo(jogo: JogoBase):
    collection = mongodb.get_collection()
    jogo_dict = jogo.model_dump()
    resultado = collection.insert_one(jogo_dict)
    jogo_criado = collection.find_one({"_id": resultado.inserted_id})
    jogo_criado["_id"] = str(jogo_criado["_id"])
    return jogo_criado

@app.get("/jogos/", response_model=list[JogoResponse])
async def listar_jogos(plataforma: str = None, status: str = None):
    collection = mongodb.get_collection()
    filtro = {}
    if plataforma:
        filtro["plataforma"] = plataforma.upper()
    if status:
        filtro["status"] = {"$regex": status, "$options": "i"}
    
    jogos = list(collection.find(filtro))
    for jogo in jogos:
        jogo["_id"] = str(jogo["_id"])
    return jogos

@app.get("/jogos/{jogo_id}", response_model=JogoResponse)
async def buscar_jogo(jogo_id: str):
    collection = mongodb.get_collection()
    if not ObjectId.is_valid(jogo_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    jogo = collection.find_one({"_id": ObjectId(jogo_id)})
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    jogo["_id"] = str(jogo["_id"])
    return jogo

@app.put("/jogos/{jogo_id}")
async def atualizar_jogo(jogo_id: str, jogo_atualizado: JogoBase):
    collection = mongodb.get_collection()
    if not ObjectId.is_valid(jogo_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    resultado = collection.update_one(
        {"_id": ObjectId(jogo_id)},
        {"$set": jogo_atualizado.model_dump()}
    )
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    return {"mensagem": "Jogo atualizado!", "id": jogo_id}

@app.delete("/jogos/{jogo_id}")
async def remover_jogo(jogo_id: str):
    collection = mongodb.get_collection()
    if not ObjectId.is_valid(jogo_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    resultado = collection.delete_one({"_id": ObjectId(jogo_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    return {"mensagem": "Jogo removido!"}

@app.get("/estatisticas")
async def estatisticas():
    """Professor, endpoint extra pra mostrar dados legais"""
    collection = mongodb.get_collection()
    jogos = list(collection.find())
    
    if not jogos:
        return {"mensagem": "Biblioteca vazia! 🎮"}
    
    total_gasto = sum(j.get("valor_pago", 0) for j in jogos)
    total_horas = sum(j.get("horas_jogadas", 0) for j in jogos)
    total_jogos = len(jogos)
    
    ps4 = sum(1 for j in jogos if j.get("plataforma") == "PS4")
    ps5 = sum(1 for j in jogos if j.get("plataforma") == "PS5")
    
    fisica = sum(1 for j in jogos if "Física" in j.get("tipo_midia", ""))
    digital = sum(1 for j in jogos if "Digital" in j.get("tipo_midia", ""))
    
    completos = sum(1 for j in jogos if "Completo" in j.get("status", "") or "Platinado" in j.get("status", ""))
    
    return {
        "total_jogos": total_jogos,
        "total_gasto": round(total_gasto, 2),
        "total_horas": round(total_horas, 1),
        "valor_medio": round(total_gasto / total_jogos, 2) if total_jogos > 0 else 0,
        "custo_por_hora": round(total_gasto / total_horas, 2) if total_horas > 0 else 0,
        "por_plataforma": {"PS4": ps4, "PS5": ps5},
        "por_midia": {"Física": fisica, "Digital": digital},
        "completos": completos,
        "percentual_completo": round((completos / total_jogos) * 100, 1) if total_jogos > 0 else 0
    }

@app.get("/health")
async def health_check():
    return {"status": "🎮 Online!", "mongodb": "conectado"}