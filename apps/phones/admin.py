from django.contrib import admin

from apps.phones.models import Phones


class PhoneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone",
        "phone_type",
    )
    search_fields = ("phone", "phone_type")
    ordering = ("phone",)


admin.site.register(Phones, PhoneAdmin)
