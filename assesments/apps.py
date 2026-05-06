from django.apps import AppConfig


class AssesmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assesments'

    def ready(self):
        try:
            from .scheduler import start_scheduler
            start_scheduler()
        except Exception as e:
            # prevents crash during migrations / startup
            print(f"Scheduler failed to start: {e}")