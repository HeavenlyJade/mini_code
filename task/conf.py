from environs import Env
from celery.schedules import crontab

env = Env()
env.read_env(override=True)

broker_url = env.str('CELERY_BROKER_URL')
result_backend = env.str('CELERY_RESULT_BACKEND')
broker_transport_options = env.json('CELERY_BROKER_TRANSPORT_OPTIONS', '{}')
result_backend_transport_options = env.json('CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS', '{}')
accept_content = ['json', 'msgpack', 'pickle']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'Asia/Shanghai'
enable_utc = False
imports = ('task.log', 'task.user_log_processor')
worker_ready_handlers = ['task.user_log_processor.start_consumer']

beat_schedule = {
    'update-logistics-every-hour': {
        'task': 'task.dongwen_logistics.update_logistics_task',
        'schedule': crontab(minute=0, hour='*'),
    },
}
