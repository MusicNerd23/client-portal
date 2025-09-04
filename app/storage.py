import os
import uuid
from werkzeug.utils import secure_filename


class LocalStorage:
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.path.join(os.getcwd(), 'uploads')

    def save(self, org_slug, file_storage):
        original = secure_filename(file_storage.filename)
        name, ext = os.path.splitext(original)
        # Use a random suffix to avoid collisions and path probing
        unique = f"{name}-{uuid.uuid4().hex[:8]}{ext}"
        org_upload_folder = os.path.join(self.base_dir, org_slug)
        os.makedirs(org_upload_folder, exist_ok=True)
        file_path = os.path.join(org_upload_folder, unique)
        file_storage.save(file_path)
        return file_path, unique


def get_storage():
    # Placeholder for future S3/Backblaze selection via config
    return LocalStorage()
