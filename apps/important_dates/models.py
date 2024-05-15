from django.db import models

from apps.abstracts.models import AbstractModel

# Create your models here.


IMPORTANT_DATE_TYPE_CHOICES = {
    "BI": "Cumpleaños",
    "AN": "Aniversario",
    "OT": "Otro",
}


class ImportantDates(AbstractModel):
    important_date = models.DateField(auto_now=False, auto_now_add=False)
    important_date_type = models.CharField(
        max_length=2, choices=IMPORTANT_DATE_TYPE_CHOICES, default="BI"
    )
