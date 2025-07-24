import time
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from collections import deque
from typing import Dict, Any
import threading

class RequestLogger(BaseHTTPMiddleware):
    def __init__(self, app, max_logs: int = 1000):
        super().__init__(app)
        self.logs = deque(maxlen=max_logs)
        self.lock = threading.Lock()
    
    def add_log(self, log_entry: Dict[str, Any]):
        with self.lock:
            self.logs.append(log_entry)
    
    def get_logs(self) -> list:
        with self.lock:
            return list(self.logs)
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        timestamp = datetime.now()
        
        log_entry = {
            "timestamp": timestamp.isoformat(),
            "method": request.method,
            "path": str(request.url.path),
            "query_params": dict(request.query_params),
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown"),
            "start_time": start_time
        }
        
        print(f"*** [{timestamp.isoformat()}] Incoming {request.method} request to {request.url.path} ***")

        response = await call_next(request)
        
        # Calculate the duration of the request
        process_time = time.perf_counter() - start_time
        
        log_entry.update({
            "status_code": response.status_code,
            "duration": round(process_time, 4),
            "response_size": response.headers.get("content-length", "unknown")
        })
        
        self.add_log(log_entry)
        
        print(f"*** [{timestamp.isoformat()}] Request completed in {process_time:.4f} seconds - Status code: {response.status_code} ***")

        return response

# Instance global del logger
request_logger = RequestLogger(None)