# Inicar o Celery quando a gente subir o projeto Django

from .celery import app as celery_app

__all__ = ('celery_app',)