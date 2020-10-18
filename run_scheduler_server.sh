cd project
celery -A app.celery_app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler -S django
