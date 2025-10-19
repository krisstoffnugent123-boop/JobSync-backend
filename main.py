
from config import get_settings
from routes import auth, jobs, gigs, matching, analytics
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone


settings = get_settings()

app = FastAPI(
    title="LinkWorkJA API",
    description="AI-powered job matching platform for Jamaica",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(gigs.router)
app.include_router(matching.router)
app.include_router(analytics.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to LinkWorkJA API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)