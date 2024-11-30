import os
import shutil
import mimetypes
from pathlib import Path
from utils.logger import log
from datetime import datetime
from moviepy import VideoFileClip, AudioFileClip
from PIL import Image

# Supported media types
SUPPORTED_MEDIA = {
    "audio": ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/flac"],
    "video": ["video/mp4", "video/x-matroska", "video/x-msvideo", "video/mpeg"],
    "image": ["image/jpeg", "image/png", "image/gif", "image/tiff"]
}

def organize_media(source_dir, target_dir):
    """
    Organizes media files into directories based on type and metadata.

    Args:
        source_dir (str): The directory containing media files.
        target_dir (str): The directory to organize media files into.
    """
    if not os.path.exists(source_dir):
        log(f"Source directory '{source_dir}' does not exist.", "error")
        return

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            mime_type, _ = mimetypes.guess_type(file_path)

            if not mime_type:
                continue

            category = None
            for media_type, types in SUPPORTED_MEDIA.items():
                if mime_type in types:
                    category = media_type
                    break

            if category:
                metadata = extract_metadata(file_path, category)
                date = metadata.get("date", "unknown_date")
                target_subdir = os.path.join(target_dir, category, date)

                os.makedirs(target_subdir, exist_ok=True)
                shutil.move(file_path, os.path.join(target_subdir, file))
                log(f"Moved {file} to {target_subdir}", "info")

def extract_metadata(file_path, category):
    """
    Extracts metadata from a media file.

    Args:
        file_path (str): Path to the media file.
        category (str): The category of the media file (audio, video, image).

    Returns:
        dict: Metadata for the media file.
    """
    metadata = {"date": "unknown_date", "details": ""}

    try:
        if category == "image":
            with Image.open(file_path) as img:
                metadata["date"] = img._getexif().get(36867, "unknown_date")
                metadata["details"] = f"{img.size[0]}x{img.size[1]}"

        elif category == "video":
            with VideoFileClip(file_path) as clip:
                metadata["date"] = str(datetime.utcfromtimestamp(os.path.getmtime(file_path)))
                metadata["details"] = f"{clip.size[0]}x{clip.size[1]}, {clip.duration}s"

        elif category == "audio":
            with AudioFileClip(file_path) as clip:
                metadata["date"] = str(datetime.utcfromtimestamp(os.path.getmtime(file_path)))
                metadata["details"] = f"Duration: {clip.duration}s"

    except Exception as e:
        log(f"Failed to extract metadata for {file_path}: {e}", "error")

    return metadata

def rename_media_files(directory, pattern="{name}_{date}.{ext}"):
    """
    Renames media files in a directory based on a pattern.

    Args:
        directory (str): The directory containing media files.
        pattern (str): The renaming pattern. Default: "{name}_{date}.{ext}"
    """
    if not os.path.exists(directory):
        log(f"Directory '{directory}' does not exist.", "error")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            mime_type, _ = mimetypes.guess_type(file_path)

            if not mime_type:
                continue

            name, ext = os.path.splitext(file)
            metadata = extract_metadata(file_path, "unknown")
            date = metadata.get("date", "unknown_date").replace(":", "-").split(" ")[0]

            new_name = pattern.format(name=name, date=date, ext=ext.lstrip("."))
            new_path = os.path.join(root, new_name)

            os.rename(file_path, new_path)
            log(f"Renamed {file} to {new_name}", "info")

def convert_media(source_file, target_file, target_format):
    """
    Converts a media file to a different format.

    Args:
        source_file (str): Path to the source file.
        target_file (str): Path to save the converted file.
        target_format (str): Format to convert to (e.g., 'mp3', 'mp4', 'png').
    """
    try:
        mime_type, _ = mimetypes.guess_type(source_file)

        if not mime_type:
            log(f"Unsupported file type for {source_file}.", "error")
            return

        if mime_type.startswith("video"):
            with VideoFileClip(source_file) as clip:
                if target_format == "mp3":
                    clip.audio.write_audiofile(target_file)
                else:
                    clip.write_videofile(target_file)
        elif mime_type.startswith("audio"):
            with AudioFileClip(source_file) as clip:
                clip.write_audiofile(target_file)
        elif mime_type.startswith("image"):
            with Image.open(source_file) as img:
                img.save(target_file)

        log(f"Converted {source_file} to {target_format}.", "info")
    except Exception as e:
        log(f"Failed to convert {source_file}: {e}", "error")

def backup_media(source_dir, backup_dir):
    """
    Backs up media files from source to a backup directory.

    Args:
        source_dir (str): The source directory containing media files.
        backup_dir (str): The backup directory.
    """
    if not os.path.exists(source_dir):
        log(f"Source directory '{source_dir}' does not exist.", "error")
        return

    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_subdir = os.path.join(backup_dir, f"backup_{timestamp}")

    shutil.copytree(source_dir, backup_subdir)
    log(f"Backed up media files to {backup_subdir}.", "info")
