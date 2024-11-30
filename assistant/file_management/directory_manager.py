import os
import shutil
import time
import zipfile
import hashlib
import boto3  # For cloud upload (Amazon S3 example)

# Configuration
SOURCE_DIR = "files_to_manage/"
ARCHIVE_DIR = "archived_files/"
BACKUP_DIR = "backups/"
LOG_DIR = "logs/"
AGE_LIMIT_DAYS = 30  # For deleting old files

# Cloud Storage Configuration (for AWS S3)
AWS_S3_BUCKET = "your-bucket-name"
AWS_ACCESS_KEY = "your-access-key"
AWS_SECRET_KEY = "your-secret-key"

# File Categories
FILE_CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "videos": [".mp4", ".avi", ".mkv"],
    "audio": [".mp3", ".wav"],
}

def organize_files():
    """
    Organize files in the source directory into subdirectories based on file type.
    """
    try:
        if not os.path.exists(SOURCE_DIR):
            raise FileNotFoundError(f"Source directory {SOURCE_DIR} not found")

        for filename in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, filename)
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(filename)[1].lower()

                for category, extensions in FILE_CATEGORIES.items():
                    if file_extension in extensions:
                        category_dir = os.path.join(SOURCE_DIR, category)
                        if not os.path.exists(category_dir):
                            os.makedirs(category_dir)
                        shutil.move(file_path, os.path.join(category_dir, filename))
                        print(f"Moved {filename} to {category} folder")
                        break
    except Exception as e:
        print(f"Error in organizing files: {str(e)}")

def move_old_files():
    """
    Move files older than the specified age limit to an archive directory.
    """
    try:
        current_time = time.time()
        if not os.path.exists(ARCHIVE_DIR):
            os.makedirs(ARCHIVE_DIR)

        for filename in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                file_age_days = file_age / (60 * 60 * 24)

                if file_age_days > AGE_LIMIT_DAYS:
                    shutil.move(file_path, os.path.join(ARCHIVE_DIR, filename))
                    print(f"Moved {filename} to archive folder")
    except Exception as e:
        print(f"Error in moving old files: {str(e)}")

def compress_files():
    """
    Compress files into a zip archive for storage or backup.
    """
    try:
        if not os.path.exists(SOURCE_DIR):
            raise FileNotFoundError(f"Source directory {SOURCE_DIR} not found")

        zip_filename = os.path.join(BACKUP_DIR, f"archive_{time.strftime('%Y%m%d_%H%M%S')}.zip")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(SOURCE_DIR):
                for file in files:
                    zipf.write(os.path.join(root, file), file)
        print(f"Files compressed to {zip_filename}")
    except Exception as e:
        print(f"Error in compressing files: {str(e)}")

def upload_to_cloud():
    """
    Upload files to cloud storage (AWS S3 in this case).
    """
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        for filename in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, filename)
            if os.path.isfile(file_path):
                s3.upload_file(file_path, AWS_S3_BUCKET, filename)
                print(f"Uploaded {filename} to cloud storage (S3).")
    except Exception as e:
        print(f"Error uploading to cloud: {str(e)}")

def monitor_directory():
    """
    Monitor a directory for new files and trigger actions.
    """
    try:
        # File monitoring logic (like using watchdog, or a polling mechanism)
        # For simplicity, we assume files are manually moved into the folder.
        print(f"Monitoring {SOURCE_DIR} for new files...")
        while True:
            time.sleep(5)  # Check for new files every 5 seconds
            if os.listdir(SOURCE_DIR):  # If there are any files in the directory
                organize_files()  # Call organize function or trigger any other action
    except Exception as e:
        print(f"Error in monitoring directory: {str(e)}")

if __name__ == "__main__":
    organize_files()
    move_old_files()
    compress_files()
    upload_to_cloud()
