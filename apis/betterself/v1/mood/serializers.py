from rest_framework import serializers

from events.models import UserMoodLog, INPUT_SOURCES_TUPLES


class MoodReadOnlySerializer(serializers.ModelSerializer):
    notes = serializers.CharField(required=False)

    class Meta:
        model = UserMoodLog
        fields = ('value', 'time', 'notes', 'source', 'uuid')


class MoodCreateUpdateSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=False, read_only=True)
    value = serializers.IntegerField(max_value=10, min_value=1)
    notes = serializers.CharField(required=False)
    source = serializers.ChoiceField(INPUT_SOURCES_TUPLES)

    class Meta:
        fields = ('value', 'time', 'notes', 'source', 'uuid')
        model = UserMoodLog

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model
        time = validated_data.pop('time')

        obj, created = create_model.objects.update_or_create(
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
