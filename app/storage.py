import os
from werkzeug.utils import secure_filename


class LocalStorage:
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.path.join(os.getcwd(), 'uploads')

    def save(self, org_slug, file_storage):
        filename = secure_filename(file_storage.filename)
        org_upload_folder = os.path.join(self.base_dir, org_slug)
        os.makedirs(org_upload_folder, exist_ok=True)
        file_path = os.path.join(org_upload_folder, filename)
        file_storage.save(file_path)
        return file_path, filename


def get_storage():
    # Placeholder for future S3/Backblaze selection via config
    return LocalStorage()

