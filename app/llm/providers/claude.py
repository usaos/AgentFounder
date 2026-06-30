import httpx
from app.llm.base_adapter import BaseAdapter, LLMResult
class ClaudeAdapter(BaseAdapter):
    def __init__(self, key: str, model: str):
        self.headers = {"x-api-key":key,"anthropic-version":"2023-06-01","content-type":"application/json"}
        self.model = model
    async def chat(self, prompt: str, system: str, temp: float) -> LLMResult:
        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.post("https://api.anthropic.com/v1/messages", headers=self.headers, json={"model":self.model,"system":system,"messages":[{"role":"user","content":prompt}],"temperature":temp,"max_tokens":2048})
            return LLMResult(text=r.json()["content"][0]["text"])
