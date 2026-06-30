from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.crypto import decrypt_env
class GlobalAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        env = decrypt_env()
        self.global_token = env.get("API_GLOBAL_TOKEN", "AF_DEFAULT_2026")
        self.whitelist = ["/", "/health", "/dashboard", "/docs", "/openapi.json", "/favicon.ico"]
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path == w or path.startswith(w) for w in self.whitelist):
            return await call_next(request)
        
        token_header = request.headers.get("X-Access-Token", "")
        if token_header != self.global_token:
            raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid API Global Token")
        
        return await call_next(request)
