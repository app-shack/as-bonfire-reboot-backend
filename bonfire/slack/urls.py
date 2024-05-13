from django.urls import path

from . import views

app_name = "slack"


urlpatterns = [
    path(
        "incoming-slack-event-webhook/",
        views.IncomingSlackEventWebhookView.as_view(),
        name="incoming-slack-event-webhook",
    ),
]
