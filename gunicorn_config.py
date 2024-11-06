# https://developers.redhat.com/articles/2023/08/17/how-deploy-flask-application-python-gunicorn#containerization
import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:5000')

forwarded_allow_ips = '*'

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '30'))
loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'info')
accesslog = os.environ.get('GUNICORN_ACCESS_LOG', '-')
errorlog = os.environ.get('GUNICORN_ERROR_LOG', '-')
preload_app = os.environ.get('GUNICORN_PRELOAD', 'True') == 'True'
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')
