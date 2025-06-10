import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
import asyncpg
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

# Pydantic model for request body
class Student(BaseModel):
    roll_number: int
    name: str

# PostgreSQL connection URL (e.g. postgresql://postgres:password@host:5432/postgres)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set in .env, e.g., postgresql://user:pass@host:5432/dbname")

async def init_db(pool: asyncpg.Pool):
    # Create Postgres table if not exists
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS student_record (
                roll_number INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create connection pool and init DB
    pool = await asyncpg.create_pool(DATABASE_URL)
    app.state.db_pool = pool
    await init_db(pool)
    yield
    # Shutdown: close pool
    await pool.close()

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
    pool: asyncpg.Pool = app.state.db_pool
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                "INSERT INTO student_record (roll_number, name) VALUES ($1, $2)",
                student.roll_number,
                student.name,
            )
            return {"status": "success", "message": "Record added."}
        except asyncpg.UniqueViolationError:
            raise HTTPException(status_code=400, detail="Roll number already exists.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "fastapi_supabase:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
