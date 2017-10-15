from django.contrib import admin

from betterself.users.models import UserPhoneNumberDetails
from events.models import SupplementLog, DailyProductivityLog, SupplementReminder


@admin.register(SupplementLog)
class SupplementEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplement', 'quantity', 'time', 'source')
    search_fields = ('supplement__name',)

    class Meta:
        model = SupplementLog


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


admin.site.register(UserPhoneNumberDetails)
admin.site.register(SupplementReminder)
