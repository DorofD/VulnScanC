from app.services.sarif.sarif_handler import SarifHandler

def upload_sarif(file):
    sh = SarifHandler()
    sh.upload_file(file)

def get_sarif_path(filename):
    sh = SarifHandler()
    return sh.get_file_path(filename)

def delete_sarif(filename):
    sh = SarifHandler()
    return sh.delete_file(filename)