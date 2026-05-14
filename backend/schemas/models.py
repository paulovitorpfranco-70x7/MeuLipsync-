from typing import Literal

from pydantic import BaseModel


JobState = Literal["pending", "processing", "completed", "failed"]


class GenerateResponse(BaseModel):
    job_id: str
    status: JobState


class JobStatus(BaseModel):
    job_id: str
    status: JobState
    progress: int = 0
    video_url: str | None = None
    error: str | None = None
