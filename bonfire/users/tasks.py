from bonfire.celery import app

from . import models


@app.task
def send_reset_password_email(user_pk):
    user = models.User.objects.get(pk=user_pk)
    user.send_password_reset_email()


@app.task
def post_process_user_profile_image_task(user_id):
    image = models.UserProfileImage.objects.get(user=user_id)
    image.post_process()


@app.task
def sync_with_slack_user_task(user_pk):
    user = models.User.objects.get(pk=user_pk)
    user.sync_with_slack()
