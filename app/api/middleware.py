from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
class LimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, req_per_min=60):
        super().__init__(app)
        self.rate = req_per_min
        self.ip_map = {}
        self.last_cleanup = time.time()
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/health", "/"]:
            return await call_next(request)
        now = time.time()
        if now - self.last_cleanup > 300:
            self.ip_map.clear()
            self.last_cleanup = now
        ip = request.client.host if request.client else "unknown"
        if ip not in self.ip_map:
            self.ip_map[ip] = []
        
        self.ip_map[ip] = [t for t in self.ip_map[ip] if now - t < 60]
        if len(self.ip_map[ip]) >= self.rate:
            return JSONResponse(status_code=429, content={"detail": "Request limit reached"})
        self.ip_map[ip].append(now)
        return await call_next(request)
