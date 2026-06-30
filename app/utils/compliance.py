import asyncio
import time
class ComplianceGuard:
    def __init__(self):
        self.last_scan = 0
        self.min_interval = 5
    async def wait_scan_cooldown(self):
        now = time.time()
        if now - self.last_scan < self.min_interval:
            await asyncio.sleep(self.min_interval - (now - self.last_scan))
        self.last_scan = time.time()
guard = ComplianceGuard()
