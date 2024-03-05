from celery.schedules import crontab

from bonfire.celery import app

from . import models


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/15"),
        refresh_door_task.s(),
    )


@app.task
def refresh_door_task():
    for door in models.Door.objects.all():
        door.refresh_status()
