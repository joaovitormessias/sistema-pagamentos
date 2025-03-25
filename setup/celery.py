import os
from celery import Celery

# Configuração padrão do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('setup')

# Usando o Redis como broker
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregar tarefas de todos os apps Django registrados
app.autodiscover_tasks()
