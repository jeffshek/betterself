from rest_framework import serializers

from betterself.utils.date_utils import get_current_utc_time_and_tz
from events.models import UserMoodLog, INPUT_SOURCES_TUPLES, WEB_INPUT_SOURCE


class MoodReadOnlySerializer(serializers.ModelSerializer):
    notes = serializers.CharField(required=False)

    class Meta:
        model = UserMoodLog
        fields = ('value', 'time', 'notes', 'source', 'uuid')


class MoodCreateUpdateSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=False, read_only=True)
    value = serializers.IntegerField(max_value=10, min_value=1)
    notes = serializers.CharField(required=False)
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE)
    time = serializers.DateTimeField(default=get_current_utc_time_and_tz)

    class Meta:
        fields = ('value', 'time', 'notes', 'source', 'uuid')
        model = UserMoodLog

    def create(self, validated_data):
        user = self.context.get('user') or self.context['request'].user
        create_model = self.Meta.model
        time = validated_data.pop('time')

        obj, _ = create_model.objects.update_or_create(
            user=user,
            time=time,
            defaults=validated_data)

        return obj

    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        instance.source = validated_data.get('source', instance.source)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance
