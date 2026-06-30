import asyncio
import gc
from sentence_transformers import SentenceTransformer
from app.utils.logger import logger
_embed_cache = None
_load_lock = asyncio.Lock()
async def get_embedding_model():
    global _embed_cache
    async with _load_lock:
        if _embed_cache is None:
            logger.info("Loading vector model...")
            _embed_cache = SentenceTransformer("all-MiniLM-L6-v2")
        return _embed_cache
async def unload_embedding():
    global _embed_cache
    if _embed_cache:
        del _embed_cache
        _embed_cache = None
        gc.collect()
