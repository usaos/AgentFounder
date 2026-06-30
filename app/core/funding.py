from app.llm.router import llm_router
class FundingEngine:
    async def generate_proposal(self, opp: dict, team: list) -> str:
        return await llm_router.run("summary_trend", f"Pitch for {opp['pain']}").text
funding = FundingEngine()
