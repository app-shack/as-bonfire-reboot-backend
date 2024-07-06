from django.db import models
from rest_framework import serializers


class Office(models.TextChoices):
    UPPSALA = "uppsala"
    STOCKHOLM = "stockholm"


class HypeLevel(models.TextChoices):
    ZERO = "zero"
    ONE = "one"
    TWO = "two"
    THREE = "three"


class OfficeHypeSerializer(serializers.Serializer):
    location = serializers.ChoiceField(choices=Office.choices, read_only=True)
    hype_level = serializers.ChoiceField(choices=HypeLevel.choices, read_only=True)
    hype_number = serializers.IntegerField(read_only=True)


class WeekOfficeHypeSerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    hype = OfficeHypeSerializer(many=True, read_only=True)


class TodaysAttendanceSerializer(serializers.Serializer):
    total_checked_in_percentage = serializers.FloatField(read_only=True)
