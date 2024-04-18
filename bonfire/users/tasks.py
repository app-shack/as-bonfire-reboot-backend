from celery.schedules import crontab

from bonfire.celery import app

from . import models


@app.task
def send_reset_password_email(user_pk):
    user = models.User.objects.get(pk=user_pk)
    user.send_password_reset_email()


@app.task
def clear_vibe_gifs():
    models.User.objects.all().update(vibe_gif="")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="0", hour="01"), clear_vibe_gifs.s())
