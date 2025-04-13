import os
from datetime import datetime


class SarifHandler:
    def __init__(self, sarif_path='/data/sarif'):
        self.sarif_path = sarif_path
        os.makedirs(self.sarif_path, exist_ok=True)

    def upload_file(self, file, project_name):
        if not file:
            raise ValueError("No file provided for upload.")
        if not file.filename.endswith('.sarif'):
            raise ValueError(
                "Invalid file type. Only .sarif files are allowed.")
        now = datetime.now()
        formatted_time = now.strftime("%d-%m-%Y_%H-%M")
        filename = f"{project_name}_{formatted_time}.sarif"
        save_path = os.path.join(self.sarif_path, filename)
        file.save(save_path)
        return filename

    def get_file_path(self, filename):
        file_path = os.path.join(self.sarif_path, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File {filename} does not exist in {self.sarif_path}.")
        return file_path

    def get_filenames(self):
        if not os.path.exists(self.sarif_path):
            raise FileNotFoundError(f"{self.sarif_path} does not exist.")
        filenames = [file for file in os.listdir(
            self.sarif_path) if os.path.isfile(os.path.join(self.sarif_path, file))]
        return filenames

    def delete_file(self, filename):
        file_path = os.path.join(self.sarif_path, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File {filename} does not exist in {self.sarif_path}.")
        os.remove(file_path)
        return True
