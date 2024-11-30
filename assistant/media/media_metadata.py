import os
import mimetypes
from moviepy import VideoFileClip, AudioFileClip
from PIL import Image
from utils.logger import log

def extract_metadata(file_path):
    """
    Extract metadata from a media file (video, audio, image).
    """
    try:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            log(f"Unsupported file type for metadata extraction: {file_path}", "error")
            return None

        metadata = {"file_path": file_path, "type": mime_type}

        if "video" in mime_type:
            with VideoFileClip(file_path) as clip:
                metadata.update({
                    "duration": clip.duration,
                    "fps": clip.fps,
                    "resolution": f"{clip.size[0]}x{clip.size[1]}",
                })
        elif "audio" in mime_type:
            with AudioFileClip(file_path) as clip:
                metadata.update({
                    "duration": clip.duration,
                    "fps": clip.fps,
                })
        elif "image" in mime_type:
            with Image.open(file_path) as img:
                metadata.update({
                    "format": img.format,
                    "size": img.size,
                    "mode": img.mode,
                })
        else:
            log(f"No metadata extracted for file type: {mime_type}", "warning")

        return metadata
    except Exception as e:
        log(f"Error extracting metadata: {e}", "error")
        return None

def search_media_by_metadata(directory, search_params):
    """
    Search for media files in a directory that match specific metadata criteria.
    """
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            metadata = extract_metadata(file_path)
            if not metadata:
                continue

            # Check if the metadata matches the search criteria
            if all(str(metadata.get(key)) == str(value) for key, value in search_params.items()):
                results.append(metadata)

    return results

if __name__ == "__main__":
    test_file = "/Users/vishal_pansare/Downloads/images.jpeg"
    print("Metadata:", extract_metadata(test_file))
    search_results = search_media_by_metadata(".", {"type": "video/mp4"})
    print("Search Results:", search_results)
