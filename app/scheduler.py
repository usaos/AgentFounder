import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.scanner import scanner
from app.core.team_builder import team_builder
from app.core.funding import funding
from app.core.factory import factory
from app.core.operator import operator
from app.utils.db import get_pending_opps, update_opp_status
from app.utils.logger import logger
class AutoEngine:
    def __init__(self):
        self.sched = AsyncIOScheduler()
        self._cycle_lock = asyncio.Lock()
    async def full_cycle(self):
        async with self._cycle_lock:
            await scanner.scan_all_sources()
            for opp in await get_pending_opps(3):
                try:
                    await update_opp_status(opp["id"], "processing")
                    team = await team_builder.match_team(opp.get("solution_dir",""))
                    await funding.generate_proposal(opp, team)
                    prod = await factory.build_deploy(opp, team)
                    await operator.monitor_product(prod["product_id"])
                    await update_opp_status(opp["id"], "deployed")
                except Exception as e:
                    logger.error(f"Err {opp['id']}: {e}")
                    await update_opp_status(opp["id"], "error")
    async def start(self, interval=30):
        self.sched.add_job(self.full_cycle, "interval", minutes=interval, max_instances=1)
        self.sched.start()
        logger.info(f"Scheduler started, interval {interval}m")
    async def shutdown(self):
        if self.sched.running: self.sched.shutdown(wait=False)
auto_engine = AutoEngine()
