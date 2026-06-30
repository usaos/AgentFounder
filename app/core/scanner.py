import uuid
import asyncio
import numpy as np
from app.utils.crypto import get_secret
from app.utils.db import insert_opp, list_opps
from app.utils.compliance import guard
from app.utils.validator import safe_json_extract
from app.llm.router import llm_router
from app.utils.logger import logger
from app.utils.vector_loader import get_embedding_model
class OpportunityScanner:
    def __init__(self):
        self.search_queries = ["I wish there was a tool", "pain points", "missing features"]
    async def _fetch_texts(self, q: str):
        try:
            from tavily import TavilyClient
            tk = get_secret("TAVILY_API_KEY")
            if tk:
                client = TavilyClient(tk)
                loop = asyncio.get_running_loop()
                def sync_search(): return client.search(query=q, max_results=6)
                res = await loop.run_in_executor(None, sync_search)
                return [r["content"] for r in res["results"] if r.get("content")]
        except Exception as e: logger.warning(f"Tavily error {e}")
        return ["Users lack tools", "Software is bloated"]
    async def scan_single(self, q: str):
        await guard.wait_scan_cooldown()
        texts = await self._fetch_texts(q)
        prompt = f'Analyze demands JSON:{{"demographic":"people","pain":"pain","intensity":0.8,"direction":"solution"}}\nText:{" ".join(texts)}'
        result = await llm_router.run("demand_scan", prompt)
        data = safe_json_extract(result.text)
        if not data: data = {"demographic":"general","pain":"demand","intensity_score":0.6,"suggested_solution_direction":"AI"}
        # Deduplication
        embed = await get_embedding_model()
        existing = await list_opps(limit=50)
        if existing:
            curr_txt = f"{data.get('demographic','')} {data.get('pain','')}"
            old_txts = [f"{o['demographic']} {o['pain']}" for o in existing]
            loop = asyncio.get_running_loop()
            vecs = await loop.run_in_executor(None, embed.encode, old_txts + [curr_txt])
            sims = np.dot(vecs[-1:], vecs[:-1].T)[0]
            if np.max(sims) > 0.85:
                logger.info(f"Duplicate skipped. Sim: {np.max(sims):.2f}")
                return
        oid = f"opp_{uuid.uuid4().hex[:8]}"
        await insert_opp({
            "id": oid, "demographic": data.get("demographic"), "pain": data.get("pain"),
            "suggested_solution_direction": data.get("suggested_solution_direction"), 
            "intensity_score": float(data.get("intensity_score", 0.5)), "sources": texts
        })
        logger.info(f"Saved {oid}")
    async def scan_all_sources(self):
        for q in self.search_queries: await self.scan_single(q)
scanner = OpportunityScanner()
