from app.services.sarif.sarif_handler import SarifHandler


def upload_sarif(file, project_name):
    sh = SarifHandler()
    return sh.upload_file(file, project_name)


def get_sarif_filenames():
    sh = SarifHandler()
    return sh.get_filenames()


def get_sarif_path(filename):
    sh = SarifHandler()
    return sh.get_file_path(filename)


def delete_sarif(filename):
    sh = SarifHandler()
    return sh.delete_file(filename)
