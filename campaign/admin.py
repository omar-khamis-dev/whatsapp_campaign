from django.contrib import admin
from .models import Contact, Group, Campaign

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'status', 'created_at', 'last_sent_at')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('status', 'source', 'groups')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'scheduled_at', 'status')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('name', 'message_text')