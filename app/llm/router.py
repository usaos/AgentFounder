from app.llm.providers.ollama import OllamaAdapter
from app.llm.providers.claude import ClaudeAdapter
from app.llm.providers.deepseek import DeepSeekAdapter
from app.utils.crypto import get_secret
from app.utils.logger import logger
from app.utils.token_monitor import token_monitor
from app.llm.base_adapter import LLMResult
TASK_ROUTE_MAP = {
    "demand_scan": ("claude", "claude-3-5-haiku-20241022"),
    "code_gen": ("deepseek", "deepseek-coder"),
    "summary_trend": ("deepseek", "deepseek-chat"),
    "offline_default": ("ollama", "llama3.1:8b")
}
ENV_KEY_MAP = {"claude": "ANTHROPIC_API_KEY", "deepseek": "DEEPSEEK_API_KEY"}
class LLMRouter:
    def __init__(self): self.cache = {}
    def get_adapter(self, vendor: str, model: str):
        if vendor in self.cache: return self.cache[vendor]
        key = get_secret(ENV_KEY_MAP.get(vendor, ""))
        if vendor != "ollama" and not key: raise ValueError(f"Missing key for {vendor}")
        if vendor == "ollama": adp = OllamaAdapter(model)
        elif vendor == "claude": adp = ClaudeAdapter(key, model)
        elif vendor == "deepseek": adp = DeepSeekAdapter(key, model)
        else: adp = None
        if adp: self.cache[vendor] = adp
        return adp
    async def run(self, task_type: str, prompt: str, system: str = "", temp=0.3):
        if token_monitor.is_cutoff(): return LLMResult(text="Token limit reached.")
        vendor, model = TASK_ROUTE_MAP.get(task_type, TASK_ROUTE_MAP["offline_default"])
        try:
            adp = self.get_adapter(vendor, model)
            res = await adp.chat(prompt, system, temp)
            token_monitor.add_tokens(res.input_tokens, res.output_tokens)
            return res
        except Exception as e:
            logger.warning(f"LLM fail, fallback Ollama: {e}")
            try:
                f = self.get_adapter("ollama", "llama3.1:8b")
                return await f.chat(prompt, system, temp)
            except Exception: return LLMResult(text="System unavailable")
llm_router = LLMRouter()
