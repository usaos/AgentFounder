import json
import ast
import re
def safe_json_extract(raw: str) -> dict:
    patterns = [r'```json\s*(.*?)\s*```', r'```\s*(.*?)\s*```', r'\{.*\}']
    for pattern in patterns:
        try:
            match = re.search(pattern, raw, re.DOTALL)
            if match:
                content = match.group(1) if pattern.startswith('```') else match.group(0)
                return json.loads(content)
        except: continue
    return {}
def check_python_code(code: str) -> bool:
    try: ast.parse(code); return True
    except SyntaxError: return False
