from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()

# Permitir que seu front (index.html) faça requisição (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique o domínio do seu front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho do JSON (ajuste conforme necessário)
CAMINHO_JSON = r"E:\vscode_projects\geosirene_project\geosirene\backend\geosirene\dados_chuva.json"

@app.get("/dados-chuva")
def dados_chuva():
    if os.path.exists(CAMINHO_JSON):
        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados
    else:
        return {"error": "Arquivo JSON não encontrado."}

# Caminho para a pasta onde está seu index.html
CAMINHO_FRONTEND = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))

# Servir arquivos estáticos (JS, CSS, etc.)
app.mount("/static", StaticFiles(directory=CAMINHO_FRONTEND), name="static")

# Servir o index.html quando acessar a raiz "/"
@app.get("/")
def servir_index():
    return FileResponse(os.path.join(CAMINHO_FRONTEND, "index.html"))
