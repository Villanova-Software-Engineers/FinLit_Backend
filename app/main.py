from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api import topic_router, lesson_router, quiz_router

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Finlit API",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(topic_router, prefix="/api", tags=["Topics"])
app.include_router(lesson_router, prefix="/api", tags=["Lessons"])
app.include_router(quiz_router, prefix="/api", tags=["Quizzes"])

@app.get("/")
async def read_root():
    return {"message": "Finlit API is running!"}