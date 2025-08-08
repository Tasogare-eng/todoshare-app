from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TodoShare API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TodoShare API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/test")
async def api_test():
    return {"message": "API endpoint working", "version": "1.0.0"}