import os
import shutil

def create_file(filename, content=""):
    """Creates a text file with optional content."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"File '{filename}' created successfully."
    except Exception as e:
        return f"Error creating file: {e}"

def create_folder(foldername):
    """Creates a new folder."""
    try:
        os.makedirs(foldername, exist_ok=True)
        return f"Folder '{foldername}' created successfully."
    except Exception as e:
        return f"Error creating folder: {e}"

def list_files(path="."):
    """Lists files in the current or specified directory."""
    try:
        files = os.listdir(path)
        return f"Files in {path}: {', '.join(files[:10])}" + ("..." if len(files) > 10 else "")
    except Exception as e:
        return f"Error listing files: {e}"

def delete_file(filename):
    """Deletes a file after confirmation (logic handled in main)."""
    try:
        if os.path.exists(filename):
            os.remove(filename)
            return f"File '{filename}' deleted."
        else:
            return f"File '{filename}' not found."
    except Exception as e:
        return f"Error deleting file: {e}"

def rename_file(old_name, new_name):
    """Renames a file."""
    try:
        os.rename(old_name, new_name)
        return f"Renamed '{old_name}' to '{new_name}'."
    except Exception as e:
        return f"Error renaming file: {e}"
