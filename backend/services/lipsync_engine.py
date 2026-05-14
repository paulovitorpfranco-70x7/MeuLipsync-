import subprocess
from pathlib import Path


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, capture_output=True, text=True)


def generate_lipsync_clip(
    image_path: str | Path,
    audio_chunk_path: str | Path,
    style: str,
    output_path: str | Path,
) -> Path:
    """Generate one lip-sync clip.

    Current implementation is a local placeholder: static image plus audio.
    To integrate SadTalker later, replace this body with a call similar to:

    subprocess.run([
        "python", "inference.py",
        "--driven_audio", str(audio_chunk_path),
        "--source_image", str(image_path),
        "--result_dir", str(output_dir),
        "--enhancer", "gfpgan",
        "--still",
    ], cwd=SADTALKER_PATH, check=True)

    The style parameter is intentionally kept in the signature for future
    mapping to SadTalker presets.
    """
    _ = style
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    _run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(image_path),
            "-i",
            str(audio_chunk_path),
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            str(output),
        ]
    )
    return output
