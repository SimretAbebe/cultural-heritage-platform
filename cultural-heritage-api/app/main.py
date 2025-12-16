from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from app.database import engine, Base
from app.routers import auth, users, categories, heritage

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app with metadata for documentation
app = FastAPI(
    title="Cultural Heritage Platform API",
    description="A REST API for preserving and serving cultural heritage content including history, traditions, leaders, places, and sayings.",
    version="1.0.0",
    docs_url="/docs",  
    redoc_url="/redoc" 
)

# Configure CORS middleware to allow frontend connections

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routers
# Each router handles a specific domain of functionality
app.include_router(
    auth,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    users,
    prefix="/users",
    tags=["Users"]
)

app.include_router(
    categories,
    prefix="/categories",
    tags=["Categories"]
)

app.include_router(
    heritage,
    prefix="/heritage",
    tags=["Heritage Entries"]
)


@app.get("/")
async def root():
    """
    Root endpoint that provides basic API information.
    Useful for health checks and API discovery.
    """
    return {
        "message": "Welcome to Cultural Heritage Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
