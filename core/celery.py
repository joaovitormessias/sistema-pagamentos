# Arquivo responsável por permitir que seja executado tarefas assíncronas em segundo plano

import os

from celery import Celery

# Define a variável de ambiente 'DJANGO_SETTINGS_MODULE' para que o Django saiba onde estão as configurações.
# Isso é essencial para que o Celery saiba qual configuração do Django usar.
# 'core.settings' refere-se ao módulo de configurações do Django (geralmente `core/settings.py`).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Cria uma instância da aplicação Celery. 
# 'core' é o nome do nosso projeto Django, usado para identificar esta instância de Celery.
# Esse nome será utilizado internamente para identificar a aplicação e suas tarefas.
app = Celery('core')

# Configura o Celery para carregar as configurações do Django automaticamente.
# As configurações do Celery são definidas no arquivo settings.py do Django, 
# e todas as configurações relacionadas ao Celery devem ser prefixadas com 'CELERY_' no arquivo `settings.py`.
# Exemplo de configuração: CELERY_BROKER_URL = 'redis://localhost:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')

# O Celery irá automaticamente descobrir todas as tarefas definidas em arquivos `tasks.py` dentro dos aplicativos Django.
# O método `autodiscover_tasks()` registra todas as tarefas sem a necessidade de importá-las manualmente,
# tornando o sistema mais modular e organizado.
app.autodiscover_tasks()