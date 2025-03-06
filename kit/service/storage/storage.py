import datetime as dt
import uuid
from abc import ABCMeta, abstractmethod

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class StorageService(metaclass=ABCMeta):
    @abstractmethod
    def put_object(self, file: FileStorage) -> dict:
        ...

    @property
    def bucket_name(self) -> str:
        return current_app.config['BUCKET_NAME']

    @property
    def delimiter(self) -> str:
        return '/'

    @classmethod
    def get_object_name(cls, filename: str) -> str:
        """Return generate object name."""
        return f'{str(uuid.uuid4())}_{secure_filename(filename)}'

    def get_url(self, bucket_name: str, object_name: str) -> str:
        return f'{bucket_name}/{self.prefix()}/{object_name}'

    @classmethod
    def prefix(cls) -> str:
        """Get directory name as object name prefix."""
        return f'{dt.date.today().strftime("%Y-%m-%d")}'
