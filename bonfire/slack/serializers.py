from rest_framework import serializers


class IncomingSlackEventWebhookSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)
    challenge = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=("url_verification",))

    def validate(self, attrs):
        event_type = attrs["type"]

        if event_type == "url_verification":
            attrs = dict(challenge=attrs["challenge"])

        return attrs
