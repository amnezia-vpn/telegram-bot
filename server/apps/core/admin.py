from django.contrib import admin

from server.apps.core.models import Key, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "create_date")
    readonly_fields = ("id", "username", "key")


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ("id", "associated_ip", "create_date")
