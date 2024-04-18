from utils.test import SerializerTestCase

from .. import serializers


class UserMeSerializerTests(SerializerTestCase):
    serializer_class = serializers.UserMeSerializer

    def test_keys(self):
        write_fields = {"email", "first_name", "last_name", "vibe_gif"}
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = write_fields.union(
            {
                "id",
            }
        )
        self.assertReadFieldsSetEqual(read_fields)


class UserTokenObtainPairSerializerTests(SerializerTestCase):
    serializer_class = serializers.UserTokenObtainPairSerializer

    def test_keys(self):
        write_fields = {
            "token",
            "client_id",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "access",
            "refresh",
        }

        self.assertReadFieldsSetEqual(read_fields)
