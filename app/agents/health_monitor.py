import asyncio
import time
from app.utils.db import get_all_agents, update_agent_health
from app.utils.logger import logger
async def start_health_monitor():
    while True:
        await asyncio.sleep(300)
        agents = await get_all_agents()
        for a in agents:
            if time.time() - a.get("last_ping", 0) > 600:
                await update_agent_health(a["agent_id"], "offline")
