from utils.test import SerializerTestCase

from .. import serializers


class AccessTokenSerializerTests(SerializerTestCase):
    serializer_class = serializers.AccessTokenSerializer

    def test_key(self):
        self.assertWriteFieldsSetEqual(set())
        read_fields = {
            "refresh",
            "access",
        }
        self.assertReadFieldsSetEqual(read_fields)


class UserMeSerializerTests(SerializerTestCase):
    serializer_class = serializers.UserMeSerializer

    def test_keys(self):
        write_fields = {
            "email",
            "first_name",
            "last_name",
        }
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = write_fields.union(
            {
                "id",
            }
        )
        self.assertReadFieldsSetEqual(read_fields)
