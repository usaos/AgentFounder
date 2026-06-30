from app.utils.db import get_product_metrics
from app.utils.logger import logger
class OperationLoop:
    async def monitor_product(self, pid: str):
        m = await get_product_metrics(pid)
        logger.info(f"Prod {pid}: {m['status']}")
operator = OperationLoop()
