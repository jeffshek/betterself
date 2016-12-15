from django.contrib import admin

from events.models import SupplementEvent


@admin.register(SupplementEvent)
class SupplementEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplement_product', 'quantity', 'time', 'source')

    class Meta:
        model = SupplementEvent
