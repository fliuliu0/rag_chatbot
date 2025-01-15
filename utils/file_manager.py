import os
import json

def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists. If it doesn't, create it.
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    except Exception as e:
        print(f"Error creating directory {directory_path}: {e}")

def read_json(file_path):
    """
    Read a JSON file and return its content as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {file_path}: {e}")
    return None

def write_json(file_path, data):
    """
    Write a dictionary to a JSON file.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing JSON to file {file_path}: {e}")

def clear_directory(directory_path):
    """
    Delete all files and subdirectories in a directory.
    """
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
    except Exception as e:
        print(f"Error clearing directory {directory_path}: {e}")

def list_files_in_directory(directory_path, extension=None):
    """
    List all files in a directory. Optionally, filter by file extension.
    """
    try:
        if extension:
            return [f for f in os.listdir(directory_path) if f.endswith(extension)]
        return os.listdir(directory_path)
    except Exception as e:
        print(f"Error listing files in directory {directory_path}: {e}")
        return []

def read_text_file(file_path):
    """
    Read a plain text file and return its content as a string.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return None

def write_text_file(file_path, content):
    """
    Write a string to a plain text file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
