web: gunicorn nvuptime.wsgi
worker: ./manage.py celery worker --beat --concurrency=2