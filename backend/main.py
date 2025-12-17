from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load API key dari .env
load_dotenv()
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
if not QWEN_API_KEY:
    raise RuntimeError("API key Qwen belum di-set di .env!")

app = FastAPI(title="Chatbot Kampus Vokasi Backend")

class ChatRequest(BaseModel):
    message: str
    context: str = ""  # optional, bisa dikirim dari frontend

@app.post("/chat")
def chat(req: ChatRequest):
    prompt = f"{req.context}\nUser: {req.message}" if req.context else req.message
    url = "https://router.huggingface.co/api/chat/completions"  # endpoint Qwen terbaru
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "Qwen/Qwen-7B-Chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_new_tokens": 200
    }
    try:
        res = requests.post(url, headers=headers, json=data, timeout=90)
        res.raise_for_status()
        response_json = res.json()
        # ambil konten response
        content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        return {"reply": content}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
