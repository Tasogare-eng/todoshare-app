from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import auth, todos, categories
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print(f"CORS allowed origins: {settings.ALLOWED_ORIGINS}")

app = FastAPI(
    title="TodoShare API",
    description="A collaborative todo list application API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
if "*" in cors_origins:
    # If wildcard, use it alone
    cors_origins = ["*"]
else:
    # Add common origins
    cors_origins.extend([
        "http://localhost:3000",
        "http://localhost:3001",
        "https://todoshare-app.vercel.app"
    ])

logger.info(f"CORS origins configured: {cors_origins}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

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

@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    """Handle CORS preflight requests"""
    return {"message": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)