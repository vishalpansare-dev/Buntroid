import os

def create_directory(path):
    os.makedirs(path, exist_ok=True)
    return f"Directory {path} created."

def delete_directory(path):
    try:
        os.rmdir(path)
        return f"Directory {path} deleted."
    except Exception as e:
        return f"Error: {e}"

def search_file(file_name, root_dir="."):
    results = []
    for root, dirs, files in os.walk(root_dir):
        if file_name in files:
            results.append(os.path.join(root, file_name))
    return results if results else ["File not found."]
