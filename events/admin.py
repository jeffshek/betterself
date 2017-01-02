from django.contrib import admin

from events.models import SupplementEvent


@admin.register(SupplementEvent)
class SupplementEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplement', 'quantity', 'time', 'source')
    search_fields = ('supplement__name', )

    class Meta:
        model = SupplementEvent
