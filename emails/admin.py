from django.contrib import admin
from .models import List, Subscriber, Email, EmailTracking, Sent
# Register your models here.

class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscriber', 'unique_id', 'opened_at', 'clicked_at')
    search_fields = ('email', 'subscriber', 'unique_id')
    # list_filter = ('email', 'subscriber', 'opened_at', 'clicked_at')

admin.site.register(List)
admin.site.register(Subscriber)
admin.site.register(Email)
admin.site.register(EmailTracking, EmailTrackingAdmin)
admin.site.register(Sent)