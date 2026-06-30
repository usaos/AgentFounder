import httpx
from app.llm.base_adapter import BaseAdapter, LLMResult
class DeepSeekAdapter(BaseAdapter):
    def __init__(self, key: str, model: str):
        self.headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        self.model = model
    async def chat(self, prompt: str, system: str, temp: float) -> LLMResult:
        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.post("https://api.deepseek.com/v1/chat/completions", headers=self.headers, json={"model":self.model,"messages":[{"role":"system","content":system},{"role":"user","content":prompt}],"temperature":temp})
            return LLMResult(text=r.json()["choices"][0]["message"]["content"])
