from rest_framework import serializers

from supplements.models import Supplement


class SupplementEventSerializer(serializers.Serializer):
    supplement_product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.FloatField(default=1)
    time = serializers.DateTimeField()
    id = serializers.IntegerField(required=False)

    def validate_supplement_product(self, value):
        user = self.context['request'].user
        user_viewable_supplements = Supplement.get_user_viewable_objects(user)
        valid_supplement_ids = user_viewable_supplements.values_list('id', flat=True)
        if value not in valid_supplement_ids:
            raise serializers.ValidationError('Invalid Supplement Product Id')

    def create(self, validated_data):
        user = self.context['request'].user
        create_model = self.context['view'].model

        # hardcode this for now
        source = 'web'

        obj, _ = create_model.objects.get_or_create(user=user, source=source,
            **validated_data)
        return obj
