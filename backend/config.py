from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
TEMP_DIR = BASE_DIR / "temp"
IMAGES_DIR = UPLOADS_DIR / "images"
AUDIO_DIR = UPLOADS_DIR / "audio"

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav"}
VALID_DURATIONS = {8, 15, 30, 60}
VALID_STYLES = {"natural", "emocional", "intenso"}
MAX_CHUNK_DURATION = 10


def ensure_directories() -> None:
    for directory in (IMAGES_DIR, AUDIO_DIR, OUTPUTS_DIR, TEMP_DIR):
        directory.mkdir(parents=True, exist_ok=True)
