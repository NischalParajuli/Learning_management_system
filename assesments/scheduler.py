from apscheduler.schedulers.background import BackgroundScheduler
import logging

from assesments.services import check_assignment_deadlines

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def start_scheduler():
    if scheduler.get_jobs():
        # already running
        return

    scheduler.add_job(
        check_assignment_deadlines,
        'interval',
        minutes=30,
        id='assignment_reminder_job',
        replace_existing=True
    )

    scheduler.start()

    logger.info("APSceduler started successfully")