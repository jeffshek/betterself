from rest_framework import serializers

from supplements.models import Supplement


class SupplementEventSerializer(serializers.Serializer):
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
