from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from config import (
    ALLOWED_AUDIO_EXTENSIONS,
    ALLOWED_IMAGE_EXTENSIONS,
    AUDIO_DIR,
    IMAGES_DIR,
    OUTPUTS_DIR,
    VALID_DURATIONS,
    VALID_STYLES,
)
from schemas.models import GenerateResponse, JobStatus
from services.video_composer import process_full_pipeline
from utils.file_manager import save_upload, validate_file_extension


router = APIRouter(prefix="/api", tags=["generation"])

jobs: dict[str, JobStatus] = {}


@router.post("/generate", response_model=GenerateResponse)
async def generate_video(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
    duration: int = Form(...),
    style: str = Form(...),
) -> GenerateResponse:
    if not validate_file_extension(image.filename or "", ALLOWED_IMAGE_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Imagem inválida. Use PNG, JPG ou JPEG.",
        )

    if not validate_file_extension(audio.filename or "", ALLOWED_AUDIO_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Áudio inválido. Use MP3 ou WAV.",
        )

    if duration not in VALID_DURATIONS:
        raise HTTPException(
            status_code=400,
            detail="Duração inválida. Use 8, 15, 30 ou 60 segundos.",
        )

    if style not in VALID_STYLES:
        raise HTTPException(
            status_code=400,
            detail="Estilo inválido. Use natural, emocional ou intenso.",
        )

    job_id = uuid4().hex
    image_path = await save_upload(image, IMAGES_DIR)
    audio_path = await save_upload(audio, AUDIO_DIR)

    jobs[job_id] = JobStatus(job_id=job_id, status="pending", progress=0)
    background_tasks.add_task(
        process_full_pipeline,
        job_id,
        image_path,
        audio_path,
        duration,
        style,
        jobs,
    )

    return GenerateResponse(job_id=job_id, status="pending")


@router.get("/status/{job_id}", response_model=JobStatus)
def get_status(job_id: str) -> JobStatus:
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job não encontrado.")
    return job


@router.get("/download/{job_id}")
def download_video(job_id: str) -> FileResponse:
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job não encontrado.")

    if job.status != "completed":
        raise HTTPException(status_code=409, detail="Vídeo ainda não está pronto.")

    video_path = OUTPUTS_DIR / f"{job_id}.mp4"
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo de vídeo não encontrado.")

    return FileResponse(
        Path(video_path),
        media_type="video/mp4",
        filename=f"lipsync-{job_id}.mp4",
    )
