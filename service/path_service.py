from log import logger
from pathlib import Path


def get_project_root():
    return Path(__file__).resolve().parent.parent.parent

def get_video_path():
    project_root = get_project_root()
    video_path = project_root / "video"
    video_path.mkdir(exist_ok=True)
    logger.error(video_path)
    return str(video_path)

def get_ffmpeg_path():
    project_root = get_project_root()
    ffmpeg_path = project_root / "ffmpeg/bin/ffmpeg.exe"
    return str(ffmpeg_path)

if __name__ == '__main__':
    print(get_video_path())