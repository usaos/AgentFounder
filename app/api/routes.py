import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.api.models import RegAgentReq, BuildTeamReq, DeployReq, FeedbackReq
from app.agents.registry import registry
from app.core.scanner import scanner
from app.core.team_builder import team_builder
from app.core.factory import factory
from app.core.meaning import oracle
from app.utils.db import list_opps, get_opp, insert_feedback, get_product_metrics
from app.agents.mesh_bus import mesh
router = APIRouter(prefix="/api/v1")
@router.post("/agents/register")
async def reg_agent(req: RegAgentReq):
    await registry.register(req.model_dump())
    return {"msg": "registered"}
@router.get("/agents")
async def list_agents():
    return {"agents": await registry.list_all()}
@router.get("/opportunities/scan")
async def scan_opp(q: str = "I wish there was an app"):
    await scanner.scan_single(q)
    return {"status": "scanned"}
@router.get("/opportunities")
async def get_opps(limit: int = 10):
    return {"opportunities": await list_opps(limit)}
@router.post("/team/build")
async def build_team(req: BuildTeamReq):
    opp = await get_opp(req.opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    team = await team_builder.match_team(opp["suggested_solution_direction"], req.max_agents)
    return {"team": team}
@router.post("/product/deploy")
async def deploy_prod(req: DeployReq):
    opp = await get_opp(req.opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    team = await team_builder.match_team(opp["suggested_solution_direction"])
    prod = await factory.build_deploy(opp, team, req.template)
    return prod
@router.post("/feedback")
async def add_feedback(req: FeedbackReq):
    score = await oracle.compute(req.text)
    await insert_feedback({
        "product_id": req.product_id, 
        "user_id": req.user_id, 
        "text": req.text, 
        "relief_score": score
    })
    return {"relief_score": score}
@router.get("/products/{pid}/metrics")
async def metrics(pid: str):
    return await get_product_metrics(pid)
@router.websocket("/ws/{agent_id}")
async def ws_stream(ws: WebSocket, agent_id: str):
    await ws.accept()
    await mesh.register_ws(agent_id, ws)
    try:
        while True:
            raw = await ws.receive_text()
            await ws.send_text(json.dumps({"ack": raw}))
    except WebSocketDisconnect:
        pass
    except Exception as e:
        pass
    finally:
        await mesh.unregister(agent_id)
