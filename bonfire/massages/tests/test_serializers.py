from utils.test import SerializerTestCase

from .. import serializers


class MassageQueueUserProfileImageSerializerTests(SerializerTestCase):
    serializer_class = serializers.MassageQueueUserProfileImageSerializer

    def test_keys(self):
        self.assertWriteFieldsSetEqual(set())
        read_fields = {
            "normal",
            "updated_at",
        }
        self.assertReadFieldsSetEqual(read_fields)


class MassageQueueUserSerializerTests(SerializerTestCase):
    serializer_class = serializers.MassageQueueUserSerializer

    def test_keys(self):
        self.assertWriteFieldsSetEqual(set())
        read_fields = {
            "id",
            "first_name",
            "last_name",
            "profile_image",
        }
        self.assertReadFieldsSetEqual(read_fields)


class MassageQueueEntrySerializerTests(SerializerTestCase):
    serializer_class = serializers.MassageQueueEntrySerializer

    def test_keys(self):
        self.assertWriteFieldsSetEqual(set())
        read_fields = {
            "id",
            "status",
            "queue_position",
            "user",
        }
        self.assertReadFieldsSetEqual(read_fields)
