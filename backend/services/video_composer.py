import subprocess
from pathlib import Path
from typing import cast

from config import MAX_CHUNK_DURATION, OUTPUTS_DIR
from schemas.models import JobState, JobStatus
from services.audio_processor import split_audio_chunks, trim_audio
from services.lipsync_engine import generate_lipsync_clip
from utils.file_manager import cleanup_temp, create_job_temp_dir


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, capture_output=True, text=True)


def _set_job(
    jobs_dict: dict[str, JobStatus],
    job_id: str,
    status: JobState,
    progress: int,
    video_url: str | None = None,
    error: str | None = None,
) -> None:
    jobs_dict[job_id] = JobStatus(
        job_id=job_id,
        status=status,
        progress=max(0, min(100, progress)),
        video_url=video_url,
        error=error,
    )


def concat_clips(clip_paths: list[Path], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    filelist = output.parent / "filelist.txt"
    filelist.write_text(
        "".join(f"file '{path.as_posix()}'\n" for path in clip_paths),
        encoding="utf-8",
    )

    _run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(filelist),
            "-c",
            "copy",
            str(output),
        ]
    )
    return output


def convert_to_vertical(input_path: str | Path, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    _run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            "-vf",
            "scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:-1:-1:color=black",
            "-c:v",
            "libx264",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )
    return output


def process_full_pipeline(
    job_id: str,
    image_path: Path,
    audio_path: Path,
    duration: int,
    style: str,
    jobs_dict: dict[str, JobStatus],
) -> None:
    temp_dir = create_job_temp_dir(job_id)

    try:
        _set_job(jobs_dict, job_id, "processing", 10)

        trimmed_audio = temp_dir / "trimmed.wav"
        trim_audio(audio_path, duration, trimmed_audio)
        _set_job(jobs_dict, job_id, "processing", 20)

        chunks = split_audio_chunks(trimmed_audio, MAX_CHUNK_DURATION)
        _set_job(jobs_dict, job_id, "processing", 30)

        clips_dir = temp_dir / "clips"
        clips_dir.mkdir(parents=True, exist_ok=True)
        clip_paths: list[Path] = []

        for index, chunk in enumerate(chunks):
            clip_path = clips_dir / f"clip_{index:03d}.mp4"
            clip_paths.append(generate_lipsync_clip(image_path, chunk, style, clip_path))
            chunk_progress = 30 + int(((index + 1) / len(chunks)) * 50)
            _set_job(jobs_dict, job_id, "processing", chunk_progress)

        merged_video = temp_dir / "merged.mp4"
        if len(clip_paths) == 1:
            merged_video.write_bytes(clip_paths[0].read_bytes())
        else:
            concat_clips(clip_paths, merged_video)
        _set_job(jobs_dict, job_id, "processing", 85)

        final_video = OUTPUTS_DIR / f"{job_id}.mp4"
        convert_to_vertical(merged_video, final_video)
        _set_job(jobs_dict, job_id, "processing", 95)

        _set_job(
            jobs_dict,
            job_id,
            "completed",
            100,
            video_url=f"/outputs/{final_video.name}",
        )
    except FileNotFoundError as exc:
        command_name = cast(str, exc.filename)
        _set_job(
            jobs_dict,
            job_id,
            "failed",
            100,
            error=f"Comando não encontrado: {command_name}. Verifique se FFmpeg/FFprobe estão no PATH.",
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        _set_job(jobs_dict, job_id, "failed", 100, error=message)
    except Exception as exc:  # noqa: BLE001 - surface background task errors to UI.
        _set_job(jobs_dict, job_id, "failed", 100, error=str(exc))
    finally:
        cleanup_temp(job_id)
