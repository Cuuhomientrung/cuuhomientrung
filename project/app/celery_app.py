from django.conf import settings
from celery import Celery
import os 
# Set default Django settings 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings') 
app = Celery(include=['app.business'])   
# Celery will apply all configuration keys with defined namespace  
app.config_from_object('django.conf:settings', namespace='CELERY')   
app.conf.task_default_queue = 'youtube-check.task'
# Load tasks from all registered apps 
app.autodiscover_tasks()
