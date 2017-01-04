from rest_framework import serializers

from apis.betterself.v1.supplements.serializers import SupplementReadOnlySerializer
from supplements.models import Supplement


class SupplementEventCreateSerializer(serializers.Serializer):
    supplement_uuid = serializers.UUIDField(source='supplement.uuid')
    quantity = serializers.FloatField(default=1)
    time = serializers.DateTimeField()
    source = serializers.CharField()
    uuid = serializers.UUIDField(required=False)

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model

        supplement_uuid = validated_data.pop('supplement')['uuid']
        supplement = Supplement.objects.get(uuid=supplement_uuid)

        quantity = validated_data.pop('quantity')
        time = validated_data.pop('time')

        obj, _ = create_model.objects.get_or_create(user=user, quantity=quantity,
            time=time, supplement=supplement, **validated_data)
        return obj


class SupplementEventReadOnlySerializer(serializers.Serializer):
    supplement = SupplementReadOnlySerializer()
    quantity = serializers.FloatField()
    time = serializers.DateTimeField()
    source = serializers.CharField()
    uuid = serializers.UUIDField()
