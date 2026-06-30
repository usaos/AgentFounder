import os, httpx
from app.llm.base_adapter import BaseAdapter, LLMResult
class OllamaAdapter(BaseAdapter):
    def __init__(self, model: str):
        self.host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        self.model = model
    async def chat(self, prompt: str, system: str, temp: float) -> LLMResult:
        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.post(f"{self.host}/api/generate", json={"model":self.model,"prompt":prompt,"system":system,"temperature":temp,"stream":False})
            return LLMResult(text=r.json().get("response",""))
