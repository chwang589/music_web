from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routes import auth, news

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music Web API",
    description="Backend API for Music Web application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173",
        "*"  # Allow all origins for development - change this in production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(news.router, prefix="/api/news", tags=["news"])

@app.get("/")
def root():
    return {"message": "Music Web API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}