from django.db import models

from apps.abstracts.models import AbstractModel

# Create your models here.


TAG_CHOICES = {
    "CU": "Clientes",
    "FR": "Amigos",
    "PR": "Proveedores",
}


class Tags(AbstractModel):
    tag = models.CharField(max_length=2, choices=TAG_CHOICES, default="FR")
