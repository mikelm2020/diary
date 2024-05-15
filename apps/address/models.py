from django.db import models

from apps.abstracts.models import AbstractModel

# Create your models here.


ADDRESS_TYPE_CHOICES = {
    "MA": "Principal",
    "WO": "Trabajo",
    "OT": "Otro",
}


class Address(AbstractModel):
    address = models.CharField(max_length=250)
    address_type = models.CharField(
        max_length=2, choices=ADDRESS_TYPE_CHOICES, default="MA"
    )
