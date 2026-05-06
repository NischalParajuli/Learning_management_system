# assessments/management/commands/send_reminders.py
from django.core.management.base import BaseCommand
from assesments.services import check_deadlines_and_send_emails


class Command(BaseCommand):
    help = 'Check deadlines and send reminder emails to students'

    def handle(self, *args, **kwargs):
        self.stdout.write('Running deadline check...')
        check_deadlines_and_send_emails()
        self.stdout.write(self.style.SUCCESS('Done.'))