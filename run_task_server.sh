cd project
celery -A app.celery_app worker --autoscale=1,1 --loglevel=DEBUG
