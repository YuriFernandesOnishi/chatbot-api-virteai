from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# COLOQUE SUA CHAVE AQUI (APENAS TESTE)
API_KEY = "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"
MODEL = "meta-llama/llama-3-8b-instruct"

app = FastAPI(title="VirTEAi Chatbot API")

# Libera acesso para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois você restringe para seu domínio
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
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um assistente educativo, acolhedor e informativo da VirTEAi. "
        "Responda dúvidas gerais sobre o Transtorno do Espectro Autista (TEA) "
        "de forma clara, respeitosa, empática e baseada em informações científicas. "
        "Nunca realize diagnósticos e sempre deixe claro que suas respostas "
        "não substituem avaliação de profissionais de saúde.\n\n"

        "Sobre a VirTEAi:\n"
        "A VirTEAi é uma plataforma tecnológica que utiliza realidade virtual "
        "e tecnologias como eye tracking para criar simulações imersivas "
        "que auxiliam profissionais especializados na coleta de dados "
        "comportamentais relacionados ao TEA. "
        "A plataforma não realiza diagnóstico, mas apoia profissionais "
        "na análise de padrões de atenção e interação.\n\n"

        "Se perguntarem sobre a VirTEAi, explique de forma clara o propósito "
        "da plataforma, sua tecnologia e seu foco em apoio profissional. "
        "Se perguntarem sobre diagnóstico individual, oriente procurar "
        "profissional especializado."
                )
            },
            {
                "role": "user",
                "content": request.message
            }
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=result)

        return {
            "response": result["choices"][0]["message"]["content"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))