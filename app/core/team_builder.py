import numpy as np
import asyncio
from app.utils.db import get_all_agents, update_agent_health
from app.utils.logger import logger
from app.utils.vector_loader import get_embedding_model, unload_embedding
class TeamBuilder:
    async def match_team(self, demand: str, top_k=3):
        embed = await get_embedding_model()
        agents = await get_all_agents()
        online_agents = [a for a in agents if a.get("health") == "online"]
        if not online_agents:
            return [{"agent_id":"default_coder","capabilities":["code_gen"],"reputation":0.9,"match_score":0.7}]
        
        loop = asyncio.get_running_loop()
        caps = [",".join(a["capabilities"]) for a in online_agents]
        cap_vecs = await loop.run_in_executor(None, embed.encode, caps)
        req_vec = await loop.run_in_executor(None, embed.encode, [demand])
        
        sims = np.dot(req_vec, cap_vecs.T)[0]
        # Weighting
        if "code" in demand.lower():
            for i, a in enumerate(online_agents):
                if "code_gen" in a["capabilities"]: sims[i] *= 1.2
                
        idx_sort = np.argsort(sims)[::-1][:min(top_k, len(online_agents))]
        result = [online_agents[i] for i in idx_sort]
        for ag in result: await update_agent_health(ag["agent_id"], "online")
        
        asyncio.create_task(unload_embedding())
        return result
team_builder = TeamBuilder()
