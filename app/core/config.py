import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_NAME: str = "FinLit API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    FIREBASE_CREDENTIALS: str = os.getenv("FIREBASE_CREDENTIALS", "")

settings = Settings()