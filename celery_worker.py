from abc import ABC

from celery import Celery, current_app
from celery.app.task import Task as BaseTask
from flask import Flask

from backend.app import create_app
from task import celery
from task import conf as task_conf


def make_celery(celery_app: Celery, flask_app: Flask):
    celery_app.config_from_object(task_conf)

    class AppContextTask(BaseTask, ABC):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    current_app.Task = AppContextTask

    return celery_app


app = create_app()

make_celery(celery, app)
