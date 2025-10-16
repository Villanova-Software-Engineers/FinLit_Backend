from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import topic_router, lesson_router, quiz_router

app = FastAPI(
    title="Finlit API",
    version="1.0.0"
)

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