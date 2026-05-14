import json
import subprocess
from pathlib import Path

from config import MAX_CHUNK_DURATION


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, capture_output=True, text=True)


def get_audio_duration(audio_path: str | Path) -> float:
    result = _run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(audio_path),
        ]
    )
    payload = json.loads(result.stdout)
    return float(payload["format"]["duration"])


def trim_audio(audio_path: str | Path, duration: int, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    _run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(audio_path),
            "-vn",
            "-t",
            str(duration),
            "-ar",
            "44100",
            "-ac",
            "2",
            str(output),
        ]
    )
    return output


def split_audio_chunks(
    audio_path: str | Path, chunk_duration: int = MAX_CHUNK_DURATION
) -> list[Path]:
    source = Path(audio_path)
    duration = get_audio_duration(source)

    if duration <= chunk_duration:
        return [source]

    chunks_dir = source.parent / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    pattern = chunks_dir / "chunk_%03d.wav"

    _run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-f",
            "segment",
            "-segment_time",
            str(chunk_duration),
            "-reset_timestamps",
            "1",
            "-vn",
            "-ar",
            "44100",
            "-ac",
            "2",
            str(pattern),
        ]
    )

    return sorted(chunks_dir.glob("chunk_*.wav"))
