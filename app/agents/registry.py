from app.utils.db import upsert_agent, get_all_agents
class AgentRegistry:
    async def register(self, data): await upsert_agent(data)
    async def list_all(self): return await get_all_agents()
registry = AgentRegistry()
