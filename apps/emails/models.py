from django.db import models

from apps.abstracts.models import AbstractModel

# Create your models here.


EMAIL_TYPE_CHOICES = {
    "MA": "Principal",
    "WO": "Trabajo",
    "OT": "Otro",
}


class Emails(AbstractModel):
    email = models.EmailField(max_length=254)
    email_type = models.CharField(
        max_length=2, choices=EMAIL_TYPE_CHOICES, default="MA"
    )
