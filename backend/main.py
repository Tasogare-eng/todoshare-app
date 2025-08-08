from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from app.core.config import settings
from app.routes import auth, todos, categories
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TodoShare API",
    description="A collaborative todo list application API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Get CORS origins from environment variable
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
logger.info(f"CORS_ORIGINS env var: {cors_origins_env}")

if cors_origins_env == "*":
    allowed_origins = ["*"]
else:
    # Split by comma and strip whitespace, removing trailing slashes
    allowed_origins = [origin.strip().rstrip("/") for origin in cors_origins_env.split(",")]
    # Add localhost for development
    allowed_origins.extend(["http://localhost:3000", "http://localhost:3001"])

logger.info(f"CORS allowed origins: {allowed_origins}")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware to ensure CORS headers are always present
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    origin = request.headers.get("origin")
    response = await call_next(request)
    
    # If origin is present and in allowed list, add CORS headers
    if origin:
        if "*" in allowed_origins or origin.rstrip("/") in [o.rstrip("/") for o in allowed_origins]:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])

@app.get("/")
async def root():
    return {"message": "TodoShare API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)