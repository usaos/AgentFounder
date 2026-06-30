from pydantic import BaseModel
class LLMResult(BaseModel):
    text: str
    input_tokens: int = 0
    output_tokens: int = 0
class BaseAdapter:
    async def chat(self, prompt: str, system: str, temp: float) -> LLMResult: raise NotImplementedError
