import uuid
import asyncio
from typing import Dict, Any
from app.utils.logger import logger
class AgentMeshBus:
    def __init__(self):
        self.ws_conns: Dict[str, Any] = {}
        self.task_queue = asyncio.Queue()
        self._shutdown_event = asyncio.Event()
    async def start(self): pass
    async def register_ws(self, aid: str, ws): self.ws_conns[aid] = ws
    async def unregister(self, aid: str): self.ws_conns.pop(aid, None)
    async def shutdown(self): self._shutdown_event.set()
mesh = AgentMeshBus()
