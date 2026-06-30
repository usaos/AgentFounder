import os
import asyncio
import shutil
import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.api.middleware import LimitMiddleware
from app.api.auth_global import GlobalAuthMiddleware
from app.utils.db import init_db, close_db, get_conn, archive_old_data
from app.scheduler import auto_engine
from app.utils.crypto import decrypt_env
from app.utils.logger import logger
from app.agents.mesh_bus import mesh
from app.agents.health_monitor import start_health_monitor
from app.core.factory import factory
from app.utils.token_monitor import token_monitor
from dashboard.app import mount_dashboard
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AgentFounder V5.0 (AGPL-3.0) 启动中...")
    await init_db()
    
    env = decrypt_env()
    
    # 启动 WebSocket 消息总线
    await mesh.start()
    
    # 启动心跳监测
    asyncio.create_task(start_health_monitor())
    
    # 启动工厂清理
    await factory.start_cleaner()
    
    # 环境变量类型安全
    cycle_enable_val = env.get("AUTO_CYCLE_ENABLE", "true")
    if isinstance(cycle_enable_val, bool):
        cycle_enable = cycle_enable_val
    else:
        cycle_enable = str(cycle_enable_val).strip().lower() == "true"
    
    if cycle_enable:
        try:
            interval = int(env.get("SCAN_INTERVAL_MIN", "30"))
        except (ValueError, TypeError):
            interval = 30
        await auto_engine.start(interval)
    # 启动月度归档任务
    auto_engine.sched.add_job(archive_old_data, 'cron', day=1, hour=2)
    # 启动每日 Token 重置
    auto_engine.sched.add_job(token_monitor.reset_daily, 'cron', hour=0)
    
    yield
    
    logger.info("正在关闭服务...")
    await auto_engine.shutdown()
    await mesh.shutdown()
    await close_db()
    logger.info("服务已安全关闭")
app = FastAPI(title="AgentFounder", version="5.0.0-AGPL", lifespan=lifespan)
# 中间件顺序：鉴权 -> 限流
app.add_middleware(GlobalAuthMiddleware)
app.add_middleware(LimitMiddleware, req_per_min=120)
app.include_router(router)
mount_dashboard(app)
@app.get("/")
async def root():
    return {"name":"AgentFounder", "license":"AGPL-3.0", "docs":"/docs", "dashboard":"/dashboard"}
@app.get("/health")
async def health():
    checks = {}
    status_code = 200
    try:
        conn = await get_conn()
        await conn.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        status_code = 503
    try:
        ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        async with httpx.AsyncClient(timeout=2) as client:
            resp = await client.get(f"{ollama_host}/api/tags")
            checks["ollama"] = "ok" if resp.status_code == 200 else "unreachable"
    except Exception:
        checks["ollama"] = "unreachable"
    try:
        _, _, free = shutil.disk_usage("/app/data")
        checks["disk_free_gb"] = round(free / (1024**3), 2)
    except Exception:
        checks["disk"] = "error"
    overall = "healthy" if "error" not in str(checks.values()) and checks.get("ollama") == "ok" else "degraded"
    return {"status": overall, "checks": checks}
