import asyncio
import aiosqlite
import json
import time
from pathlib import Path
DB_PATH = "./data/agent.db"
_db_conn: aiosqlite.Connection = None
_db_lock = asyncio.Lock()
async def init_db():
    global _db_conn
    async with _db_lock:
        if _db_conn is None:
            Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
            _db_conn = await aiosqlite.connect(DB_PATH)
            await _db_conn.execute("PRAGMA journal_mode=WAL;")
            _db_conn.row_factory = aiosqlite.Row
            
            # Creating tables
            await _db_conn.execute("CREATE TABLE IF NOT EXISTS opportunities(id TEXT PRIMARY KEY, demographic TEXT, pain TEXT, solution_dir TEXT, intensity REAL, sources TEXT, ts REAL, status TEXT DEFAULT 'scanned')")
            await _db_conn.execute("CREATE TABLE IF NOT EXISTS agents(agent_id TEXT PRIMARY KEY, capabilities TEXT, endpoint TEXT, auth_token TEXT, reputation REAL, health TEXT, last_ping REAL)")
            await _db_conn.execute("CREATE TABLE IF NOT EXISTS products(pid TEXT PRIMARY KEY, opp_id TEXT, team TEXT, deploy_url TEXT, template TEXT, avg_relief REAL, feedback_count INTEGER DEFAULT 0, ts REAL)")
            await _db_conn.execute("CREATE TABLE IF NOT EXISTS feedbacks(id INTEGER PRIMARY KEY AUTOINCREMENT, pid TEXT, user_id TEXT, content TEXT, relief REAL, ts REAL)")
            await _db_conn.execute("CREATE TABLE IF NOT EXISTS token_records(id INTEGER PRIMARY KEY, total_tokens INT, ts REAL)")
            await _db_conn.execute("CREATE TABLE IF NOT EXISTS ws_tasks(id INTEGER PRIMARY KEY, tid TEXT, agent_id TEXT, payload TEXT, status TEXT, ts REAL)")
            await _db_conn.execute("CREATE TABLE IF NOT EXISTS opp_archive(id TEXT, demographic TEXT, pain TEXT, ts REAL)")
            await _db_conn.commit()
async def close_db():
    global _db_conn
    if _db_conn:
        await _db_conn.close()
        _db_conn = None
async def get_conn():
    if _db_conn is None:
        await init_db()
    return _db_conn
async def archive_old_data():
    conn = await get_conn()
    thirty_days_ago = time.time() - (30 * 86400)
    await conn.execute("INSERT INTO opp_archive SELECT id, demographic, pain, ts FROM opportunities WHERE ts < ?", (thirty_days_ago,))
    await conn.execute("DELETE FROM opportunities WHERE ts < ?", (thirty_days_ago,))
    await conn.commit()
async def insert_token_record(total: int):
    conn = await get_conn()
    await conn.execute("INSERT INTO token_records(total_tokens, ts) VALUES (?,?)", (total, time.time()))
    await conn.commit()
async def insert_ws_task(tid: str, aid: str, payload: dict):
    conn = await get_conn()
    await conn.execute("INSERT INTO ws_tasks(tid, agent_id, payload, status, ts) VALUES (?,?,?,?,?)", 
                       (tid, aid, json.dumps(payload), "pending", time.time()))
    await conn.commit()
async def insert_opp(data: dict):
    conn = await get_conn()
    await conn.execute("INSERT INTO opportunities VALUES (?,?,?,?,?,?,?,?)", (
        data["id"], data["demographic"], data["pain"], 
        data.get("suggested_solution_direction", ""), data["intensity_score"], 
        json.dumps(data.get("sources", [])), time.time(), "scanned"
    ))
    await conn.commit()
async def list_opps(limit=10):
    conn = await get_conn()
    cursor = await conn.execute("SELECT * FROM opportunities ORDER BY intensity DESC LIMIT ?", (limit,))
    rows = await cursor.fetchall()
    return [dict(r) for r in rows]
async def get_pending_opps(limit=3):
    conn = await get_conn()
    cursor = await conn.execute("SELECT * FROM opportunities WHERE status='scanned' ORDER BY intensity DESC LIMIT ?", (limit,))
    return [dict(r) for r in await cursor.fetchall()]
async def update_opp_status(oid: str, status: str):
    conn = await get_conn()
    await conn.execute("UPDATE opportunities SET status=? WHERE id=?", (status, oid))
    await conn.commit()
async def get_opp(oid: str):
    conn = await get_conn()
    cursor = await conn.execute("SELECT * FROM opportunities WHERE id=?", (oid,))
    row = await cursor.fetchone()
    return dict(row) if row else None
async def upsert_agent(agent: dict):
    conn = await get_conn()
    await conn.execute("INSERT OR REPLACE INTO agents VALUES (?,?,?,?,?,?,?)", (
        agent["agent_id"], json.dumps(agent["capabilities"]), agent["endpoint"], 
        agent["auth_token"], agent["reputation"], agent.get("health", "online"), time.time()
    ))
    await conn.commit()
async def get_all_agents():
    conn = await get_conn()
    cursor = await conn.execute("SELECT * FROM agents")
    return [dict(r) for r in await cursor.fetchall()]
async def update_agent_health(aid: str, health: str):
    conn = await get_conn()
    await conn.execute("UPDATE agents SET health=?, last_ping=? WHERE agent_id=?", (health, time.time(), aid))
    await conn.commit()
async def insert_product(p: dict):
    conn = await get_conn()
    await conn.execute("INSERT INTO products VALUES (?,?,?,?,?,?,?,?)", (
        p["id"], p["opportunity_id"], json.dumps(p["team"]), 
        p["url"], p["template"], 0.5, 0, time.time()
    ))
    await conn.commit()
async def insert_feedback(fb: dict):
    conn = await get_conn()
    await conn.execute("INSERT INTO feedbacks (pid,user_id,content,relief,ts) VALUES (?,?,?,?,?)", (
        fb["product_id"], fb["user_id"], fb["text"], fb["relief_score"], time.time()
    ))
    await conn.commit()
async def get_product_metrics(pid: str):
    conn = await get_conn()
    cursor = await conn.execute("SELECT relief FROM feedbacks WHERE pid=?", (pid,))
    rows = await cursor.fetchall()
    scores = [r["relief"] for r in rows]
    cnt = len(scores)
    if cnt == 0: return {"count": 0, "avg_relief": 0.5, "status": "no_feedback"}
    avg = sum(scores)/cnt
    status = "healthy" if avg > 0.6 else "optimize"
    return {"count": cnt, "avg_relief": round(avg,3), "status": status}
