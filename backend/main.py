from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import OUTPUTS_DIR, UPLOADS_DIR, ensure_directories
from routers.generate import router as generate_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    ensure_directories()
    yield


app = FastAPI(title="LipSync Studio API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR, check_dir=False), name="outputs")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR, check_dir=False), name="uploads")
app.include_router(generate_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
