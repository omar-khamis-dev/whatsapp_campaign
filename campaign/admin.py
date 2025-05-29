from django.contrib import admin
from .models import Contact, Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'status', 'created_at', 'last_sent_at')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('status', 'source', 'groups')
