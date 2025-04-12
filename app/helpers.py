import zipfile
import io
import os

def unzip(zip_path: str, extract_path: str):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Extract the contents of the zip file to the specified path
            zip_file.extractall(extract_path)

        print("File extracted successfully.")
    except FileNotFoundError:
        print(f"Zip file {zip_path} not found.")
    except zipfile.BadZipFile:
        print(f"Invalid zip file {zip_path}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")