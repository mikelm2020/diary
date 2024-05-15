from django.contrib import admin

from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "is_active",
        "created",
        "updated",
    )
    search_fields = ("username",)
    ordering = ("username",)


admin.site.register(User, UserAdmin)
