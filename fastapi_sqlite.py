import os
from contextlib import asynccontextmanager

import aiosqlite
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Pydantic model for request body
class Student(BaseModel):
    roll_number: int
    name: str

DATABASE_URL = os.getenv("SQLITE_DB_PATH", "students.db")

async def init_db():
    # Create table if not exists
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS student_record (
                roll_number INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )
        await db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database
    await init_db()
    yield
    # (Optional) Shutdown actions here

app = FastAPI(lifespan=lifespan)

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add_record")
async def add_record(student: Student):
    async with aiosqlite.connect(DATABASE_URL) as db:
        try:
            await db.execute(
                "INSERT INTO student_record (roll_number, name) VALUES (?, ?)",
                (student.roll_number, student.name),
            )
            await db.commit()
            return {"status": "success", "message": "Record added."}
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="Roll number already exists.")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "fastapi_sqlite:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
