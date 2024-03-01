import sentry_sdk
from celery.schedules import crontab
from django.utils.timezone import now, timedelta
from fcm_django.models import FCMDevice

from bonfire.celery import app
from events.models import Event
from users.models import User

from . import push_notifications as pn


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/1", hour="*"), notify_events_are_starting_task.s()
    )


@app.task
def notify_events_are_starting_task():
    qs = Event.objects.filter(
        start_date__lte=now() - timedelta(minutes=1),
        starting_notification_sent_at__isnull=True,
    )

    for event in qs.iterator():
        try:
            notify_event_is_starting_task.si(event.pk).delay()
        except Exception as e:
            sentry_sdk.capture_exception(e)
        else:
            event.starting_notification_sent_at = now()
            event.save()


@app.task
def notify_event_is_starting_task(event_pk):
    event = Event.objects.select_related("office").get(pk=event_pk)

    users = User.objects.get_close_users_pks(
        event.office.latitude,
        event.office.longitude,
    )

    FCMDevice.objects.filter(user__in=list(users)).send_message(
        pn.event_is_starting(event)
    )
