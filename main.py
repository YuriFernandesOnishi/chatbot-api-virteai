from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# ⚠️ CHAVE DIRETO NO CÓDIGO (apenas para testes)
API_KEY = "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"
MODEL = "meta-llama/llama-3-8b-instruct"

app = FastAPI(title="VirTEAi Chatbot API")

# Libera acesso para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois restrinja para seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "API do Chatbot VirTEAi online 💙"}


@app.post("/chat")
def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Mensagem vazia.")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
Você é um assistente educativo, acolhedor e informativo da VirTEAi.

REGRAS IMPORTANTES:
- Sempre responda no mesmo idioma da pergunta do usuário.
- Nunca realize diagnósticos.
- Sempre deixe claro que suas respostas não substituem avaliação de profissionais de saúde.

Sobre TEA:
Responda dúvidas gerais sobre o Transtorno do Espectro Autista (TEA)
de forma clara, respeitosa, empática e baseada em informações científicas.

Sobre a VirTEAi:
A VirTEAi é uma plataforma tecnológica que utiliza realidade virtual
e tecnologias como eye tracking para criar simulações imersivas
que auxiliam profissionais especializados na coleta de dados
comportamentais relacionados ao TEA.

A plataforma não realiza diagnóstico,
mas apoia profissionais na análise de padrões de atenção e interação.

Se perguntarem sobre diagnóstico individual,
oriente procurar profissional especializado.
"""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ],
        "temperature": 0.4,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()
            )

        result = response.json()

        return {
            "response": result["choices"][0]["message"]["content"]
        }

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Timeout ao conectar com o modelo.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
