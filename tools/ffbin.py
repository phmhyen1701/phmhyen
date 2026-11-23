"""Tìm ffmpeg/ffprobe kể cả khi PATH của phiên chưa được nạp lại sau khi cài bằng winget."""
import glob
import os
import shutil


def find(name: str) -> str:
    exe = shutil.which(name)
    if exe:
        return exe
    pattern = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg*", "*", "bin", name + ".exe",
    )
    hits = sorted(glob.glob(pattern))
    if hits:
        return hits[-1]
    raise FileNotFoundError(f"Không tìm thấy {name}. Cài bằng: winget install Gyan.FFmpeg")


FFMPEG = find("ffmpeg")
FFPROBE = find("ffprobe")
