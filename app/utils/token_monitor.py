import time
import os
from app.utils.logger import logger
class TokenMonitor:
    def __init__(self):
        self.daily_limit = int(os.getenv("DAILY_TOKEN_LIMIT", "100000"))
        self.today_used = 0
        self.cutoff = False
        self.last_reset_date = time.localtime().tm_mday
    def add_tokens(self, in_tok: int, out_tok: int):
        if time.localtime().tm_mday != self.last_reset_date:
            self.reset_daily()
        total = in_tok + out_tok
        self.today_used += total
        try:
            import asyncio
            loop = asyncio.get_running_loop()
            from app.utils.db import insert_token_record
            loop.create_task(insert_token_record(total))
        except RuntimeError: pass
        if self.today_used >= self.daily_limit and not self.cutoff:
            self.cutoff = True
            logger.critical(f"Token limit reached: {self.daily_limit}")
    def is_cutoff(self) -> bool: return self.cutoff
    def reset_daily(self):
        self.today_used = 0
        self.cutoff = False
        self.last_reset_date = time.localtime().tm_mday
token_monitor = TokenMonitor()
