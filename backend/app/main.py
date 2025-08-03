from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routes import auth, news, verification

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music Web API",
    description="Backend API for Music Web application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源访问
    allow_credentials=False,  # 设为False以允许通配符origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],  # 暴露所有响应头
)

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(verification.router, prefix="/api/verification", tags=["verification"])

@app.get("/")
def root():
    return {"message": "Music Web API is running!"}

@app.get("/health")
def health_check():
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    return {
        "status": "healthy",
        "hostname": hostname,
        "local_ip": local_ip,
        "cors_enabled": True,
        "api_base": "/api"
    }