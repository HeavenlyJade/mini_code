from pathlib import Path

from flask import current_app
from werkzeug.datastructures import FileStorage

from kit.service.storage.storage import StorageService


class LocalFileStorageService(StorageService):
    def put_object(self, file: FileStorage) -> dict:
        object_name: str = self.get_object_name(file.filename)
        path: Path = Path(self.local_storage_path, self.bucket_name, self.prefix())
        if not path.exists():
            path.mkdir(parents=True)
        file.save(Path(path, object_name))
        return dict(url=self.get_url(self.bucket_name, object_name))

    @property
    def local_storage_path(self) -> Path:
        return current_app.config['LOCAL_STORAGE_PATH']
