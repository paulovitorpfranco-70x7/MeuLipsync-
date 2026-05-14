import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from config import TEMP_DIR


def validate_file_extension(filename: str, allowed: set[str]) -> bool:
    extension = Path(filename).suffix.lower().lstrip(".")
    return extension in allowed


async def save_upload(file: UploadFile, directory: Path) -> Path:
    extension = Path(file.filename or "").suffix.lower()
    filename = f"{uuid4().hex}{extension}"
    destination = directory / filename

    contents = await file.read()
    destination.write_bytes(contents)
    await file.close()

    return destination


def create_job_temp_dir(job_id: str) -> Path:
    directory = TEMP_DIR / job_id
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def cleanup_temp(job_id: str) -> None:
    shutil.rmtree(TEMP_DIR / job_id, ignore_errors=True)
