import time
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class RequestLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        timestamp = datetime.now().isoformat()
        
        print(f"*** [{timestamp}] Incoming {request.method} request to {request.url.path} ***")

        response = await call_next(request)
        # Calculate the duration of the request
        process_time = time.perf_counter() - start_time

        print(f"*** [{timestamp}] Request completed in {process_time:.4f} seconds - Status code: {response.status_code} ***")

        return response