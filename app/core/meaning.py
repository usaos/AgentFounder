import numpy as np
import asyncio
from app.utils.logger import logger
class MeaningOracle:
    def __init__(self):
        self.pos = {"great":0.9,"good":0.7}; self.neg = {"bad":-0.7}
    async def compute(self, text: str) -> float:
        s = 0.5
        txt = text.lower()
        for k,v in self.pos.items():
            if k in txt: s += v*0.1
        for k,v in self.neg.items():
            if k in txt: s += v*0.1
        return round(min(1.0, max(0.0, s)), 3)
oracle = MeaningOracle()
