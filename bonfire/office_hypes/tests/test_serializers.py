from utils.test import SerializerTestCase

from .. import serializers


class TodaysAttendanceSerializerTests(SerializerTestCase):
    serializer_class = serializers.TodaysAttendanceSerializer

    def test_keys(self):
        write_fields = set()
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "total_checked_in_percentage",
        }
        self.assertReadFieldsSetEqual(read_fields)


class OfficeHypeSerializerTests(SerializerTestCase):
    serializer_class = serializers.OfficeHypeSerializer

    def test_keys(self):
        write_fields = set()
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "location",
            "hype_level",
            "hype_number",
        }
        self.assertReadFieldsSetEqual(read_fields)


class WeekOfficeHypeSerializerTests(SerializerTestCase):
    serializer_class = serializers.WeekOfficeHypeSerializer

    def test_keys(self):
        write_fields = set()
        self.assertWriteFieldsSetEqual(write_fields)
        read_fields = {
            "date",
            "hype",
        }
        self.assertReadFieldsSetEqual(read_fields)
