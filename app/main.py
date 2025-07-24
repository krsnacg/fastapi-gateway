# from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import gateway
from app.core.logging import RequestLogger

app = FastAPI(openapi_url=None)

#predicates = [r["predicate"].replace("**", "") for r in routes]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
app.add_middleware(RequestLogger)
app.include_router(gateway.router, tags=["gateway"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
