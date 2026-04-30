#!/usr/bin/env python3
"""
Descarga un video de YouTube desde una URL y extrae fotogramas (fotos)
como archivos .jpg.

Requisitos:
  - yt-dlp instalado y en PATH
  - ffmpeg instalado y en PATH

Uso:
  python youtube_to_photos.py "https://www.youtube.com/watch?v=..." --fps 1 --output fotos
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def check_dependency(binary: str) -> None:
    if shutil.which(binary) is None:
        print(f"Error: no se encontró '{binary}' en tu PATH.", file=sys.stderr)
        sys.exit(1)


def run_command(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"Error ejecutando comando: {' '.join(cmd)}", file=sys.stderr)
        print(f"Código de salida: {exc.returncode}", file=sys.stderr)
        sys.exit(exc.returncode)


def sanitize_stem(value: str) -> str:
    # Limita caracteres problemáticos para nombres de carpeta.
    allowed = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    cleaned = "".join(ch for ch in value if ch in allowed).strip()
    return cleaned or "video"


def download_video(url: str, download_dir: Path) -> Path:
    # Descargamos en MP4 cuando sea posible.
    template = str(download_dir / "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f",
        "mp4/bestvideo+bestaudio/best",
        "--merge-output-format",
        "mp4",
        "-o",
        template,
        url,
    ]
    run_command(cmd)

    # Buscar el archivo más reciente descargado.
    videos = sorted(download_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not videos:
        # Fallback por si yt-dlp guardó otro formato.
        candidates = sorted(download_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
        files = [p for p in candidates if p.is_file()]
        if not files:
            print("Error: no se encontró el video descargado.", file=sys.stderr)
            sys.exit(1)
        return files[0]

    return videos[0]


def extract_frames(video_path: Path, output_dir: Path, fps: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # frame_%06d.jpg -> frame_000001.jpg, frame_000002.jpg, ...
    output_pattern = str(output_dir / "frame_%06d.jpg")
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(video_path),
        "-vf",
        f"fps={fps}",
        "-q:v",
        "2",
        output_pattern,
    ]
    run_command(cmd)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Descarga un video de YouTube y lo convierte en fotos (frames JPG)."
    )
    parser.add_argument("url", help="URL del video de YouTube")
    parser.add_argument(
        "--fps",
        type=float,
        default=1.0,
        help="Cantidad de fotos por segundo de video (por defecto: 1)",
    )
    parser.add_argument(
        "--output",
        default="fotos",
        help="Carpeta base de salida (por defecto: fotos)",
    )
    parser.add_argument(
        "--keep-video",
        action="store_true",
        help="Conservar el archivo de video descargado",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.fps <= 0:
        print("Error: --fps debe ser mayor que 0.", file=sys.stderr)
        sys.exit(1)

    check_dependency("yt-dlp")
    check_dependency("ffmpeg")

    work_dir = Path(args.output)
    work_dir.mkdir(parents=True, exist_ok=True)

    video_path = download_video(args.url, work_dir)
    subfolder = sanitize_stem(video_path.stem)
    frames_dir = work_dir / f"{subfolder}_frames"

    extract_frames(video_path, frames_dir, args.fps)

    if not args.keep_video and video_path.exists():
        video_path.unlink()

    print("¡Listo!")
    print(f"Frames guardados en: {frames_dir.resolve()}")


if __name__ == "__main__":
    main()
