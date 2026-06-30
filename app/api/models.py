from pydantic import BaseModel, Field
class RegAgentReq(BaseModel):
    agent_id: str
    capabilities: list[str]
    endpoint: str
    auth_token: str = ""
    reputation: float = Field(0.5, ge=0, le=1)
class BuildTeamReq(BaseModel):
    opportunity_id: str
    max_agents: int = Field(3, ge=1, le=10)
class DeployReq(BaseModel):
    opportunity_id: str
    template: str = "telegram_bot"
class FeedbackReq(BaseModel):
    product_id: str
    text: str
    user_id: str | None = "anon"
