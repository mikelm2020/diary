from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.abstracts.models import AbstractModel

# Create your models here.


PHONE_TYPE_CHOICES = {
    "MO": "Móvil",
    "WO": "Trabajo",
    "HO": "Casa",
    "MA": "Principal",
    "WF": "Fax laboral",
    "HF": "Fax de casa",
    "LO": "Localizador",
    "OT": "Otro",
}


class Phones(AbstractModel):
    phone = PhoneNumberField(blank=False)
    phone_type = models.CharField(
        max_length=2, choices=PHONE_TYPE_CHOICES, default="MO"
    )
