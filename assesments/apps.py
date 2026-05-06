from django.apps import AppConfig


class AssesmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assesments'

    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from assesments.services import check_deadlines_and_send_emails

        scheduler = BackgroundScheduler()
        scheduler.add_job(
            check_deadlines_and_send_emails,
            'interval',
            minutes=30,
            id='send_reminders',
            replace_existing=True
        )
        scheduler.start()