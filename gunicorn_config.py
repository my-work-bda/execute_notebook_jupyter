import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:5000')

forwarded_allow_ips = '*'

loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'debug')  # Set log level to DEBUG
accesslog = os.environ.get('GUNICORN_ACCESS_LOG', '-')
errorlog = os.environ.get('GUNICORN_ERROR_LOG', '-')
preload_app = os.environ.get('GUNICORN_PRELOAD', 'True') == 'True'
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')
