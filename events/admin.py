from django.contrib import admin

from betterself.users.models import UserPhoneNumber
from events.models import SupplementEvent, DailyProductivityLog, SupplementReminder


@admin.register(SupplementEvent)
class SupplementEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplement', 'quantity', 'time', 'source')
    search_fields = ('supplement__name',)

    class Meta:
        model = SupplementEvent


@admin.register(DailyProductivityLog)
class DailyProductivityLogAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'very_productive_time_minutes',
        'productive_time_minutes',
        'neutral_time_minutes',
        'distracting_time_minutes',
        'very_distracting_time_minutes',
        'user'
    ]

    class Meta:
        model = DailyProductivityLog


admin.site.register(UserPhoneNumber)
admin.site.register(SupplementReminder)
