import os

class SarifHandler:
    def __init__(self, sarif_path='/data/sarif'):
        self.sarif_path = sarif_path
        os.makedirs(self.sarif_path, exist_ok=True)

    def upload_file(self, file):
        if not file:
            raise ValueError("No file provided for upload.")
        if not file.filename.endswith('.sarif'):
            raise ValueError("Invalid file type. Only .sarif files are allowed.")
        filename = file.filename
        save_path = os.path.join(self.sarif_path, filename)
        file.save(save_path)
        return True

    def get_file_path(self, filename):
        file_path = os.path.join(self.sarif_path, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {filename} does not exist in {self.sarif_path}.")
        
        return file_path
    def delete_file(self, filename):
        file_path = os.path.join(self.sarif_path, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {filename} does not exist in {self.sarif_path}.")
        os.remove(file_path)
        return True