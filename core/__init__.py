"""Expose the Celery app so Django and the worker share task configuration."""
from .celery import app as celery_app

__all__ = ("celery_app",)
