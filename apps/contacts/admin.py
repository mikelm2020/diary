from django.contrib import admin

from apps.contacts.models import Contacts


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "last_name",
        "user",
        "get_phones_displayed",
        "created",
        "updated",
    )
    search_fields = ("name", "last_name")
    ordering = ("name",)

    def get_phones_displayed(self, obj):
        return ", ".join([str(phone.phone) for phone in obj.phones.all()])

    get_phones_displayed.short_description = "Phones"


admin.site.register(Contacts, ContactAdmin)
