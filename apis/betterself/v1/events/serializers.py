from rest_framework import serializers


class SupplementEventSerializer(serializers.Serializer):
    supplement_event_id = serializers.IntegerField(source='id')
    supplement_product_id = serializers.IntegerField()
    quantity = serializers.FloatField(default=1)
    time = serializers.DateTimeField()

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model
        return create_model(user=user, **validated_data)
