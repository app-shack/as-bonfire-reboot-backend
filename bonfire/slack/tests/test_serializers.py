from utils.test import SerializerTestCase

from .. import serializers


class IncomingSlackEventWebhookSerializerTests(SerializerTestCase):
    serializer_class = serializers.IncomingSlackEventWebhookSerializer

    def test_keys(self):
        write_fields = {
            "token",
            "challenge",
            "type",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "token",
            "challenge",
            "type",
        }
        self.assertReadFieldsSetEqual(read_fields)
