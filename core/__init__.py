# Importa a instância 'app' definida no arquivo 'celery.py' no mesmo diretório
# A instância 'app' é configurada no 'celery.py' para gerenciar tarefas assíncronas
# Renomeia a instância importada para 'celery_app' para manter a clareza sobre seu propósito
# Isso torna explícito que a variável 'celery_app' é a instância do Celery configurada.
from .celery import app as celery_app

# A variável '__all__' é uma lista especial que controla o que é exportado quando o módulo
# é importado com 'from <module> import *'.
# Neste caso, estamos explicitamente dizendo que somente a instância 'celery_app'
# será exposta para quem importar este módulo. Isso ajuda a controlar o escopo e
# a visibilidade das variáveis ou funções no módulo, evitando poluição do namespace.
__all__ = ('celery_app',)
