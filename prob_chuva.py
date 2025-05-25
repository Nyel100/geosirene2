from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretório base (onde está este script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho relativo para o JSON
CAMINHO_JSON = os.path.join(BASE_DIR, "dados_chuva.json")

@app.get("/dados-chuva")
def dados_chuva():
    if os.path.exists(CAMINHO_JSON):
        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados
    else:
        return {"error": "Arquivo JSON não encontrado."}

# Caminho para a pasta do frontend (supondo que está no mesmo nível da pasta backend)
CAMINHO_FRONTEND = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))

# Verificação se o diretório existe (evita o erro em produção)
if os.path.exists(CAMINHO_FRONTEND):
    app.mount("/static", StaticFiles(directory=CAMINHO_FRONTEND), name="static")

    @app.get("/")
    def servir_index():
        return FileResponse(os.path.join(CAMINHO_FRONTEND, "index.html"))
else:
    print(f"Diretório do frontend não encontrado: {CAMINHO_FRONTEND}")
