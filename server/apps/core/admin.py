from django.contrib import admin

from server.apps.core.models import Key, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "key", "create_date")
    readonly_fields = ("id", "username", "key")
    search_fields = ("username",)


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ("id", "associated_ip", "create_date")
    search_fields = ("associated_ip",)
