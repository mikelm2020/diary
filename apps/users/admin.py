from django.contrib import admin

from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_owner",
        "username",
        "email",
        "is_active",
        "created",
        "updated",
    )
    search_fields = ("username", "email", "is_owner")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
