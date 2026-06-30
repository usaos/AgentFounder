import uuid
import tempfile
import shutil
import subprocess
from pathlib import Path
from app.utils.db import insert_product
from app.llm.router import llm_router
from app.utils.validator import check_python_code
from app.utils.logger import logger
from app.utils.crypto import get_secret
class ProductFactory:
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
    async def start_cleaner(self): pass 
    async def _deploy_vercel(self, work_dir: Path) -> str:
        token = get_secret("VERCEL_TOKEN")
        if not token: return None
        try:
            res = subprocess.run(["vercel", "--prod", "--yes"], cwd=str(work_dir), capture_output=True, text=True, timeout=120)
            return res.stdout 
        except Exception: return None
    async def build_deploy(self, opp: dict, team: list, template="telegram_bot") -> dict:
        work_dir = Path(tempfile.mkdtemp(prefix="af_prod_"))
        try:
            src = self.template_dir / template
            shutil.copytree(src, work_dir, dirs_exist_ok=True)
            code_prompt = f"Generate {template} code for: {opp['pain']}"
            raw = await llm_router.run("code_gen", code_prompt)
            code = raw.text
            if "```" in code:
                code = code.split("```")[1].replace("python","").replace(template,"").strip()
            
            if not check_python_code(code):
                with open(src / "app.py" if template=="web_app" else src / "bot.py", "r") as f: code = f.read()
            file_name = "app.py" if template=="web_app" else "bot.py"
            (work_dir / file_name).write_text(code.replace("{{PAIN}}", opp['pain']))
            
            url = await self._deploy_vercel(work_dir) or f"file://{work_dir}"
            pid = f"prod_{uuid.uuid4().hex[:8]}"
            await insert_product({"id": pid, "opportunity_id": opp["id"], "team": team, "url": url, "template": template})
            return {"product_id": pid, "url": url}
        except Exception as e:
            shutil.rmtree(work_dir, ignore_errors=True)
            raise e
factory = ProductFactory()
