from django.db import models

from apps.abstracts.models import AbstractModel

# Create your models here.


RELATED_PERSON_TYPE_CHOICES = {
    "AS": "Asistente",
    "BR": "Hermano",
    "SO": "Hijo(a)",
    "CO": "Pareja",
    "FA": "Padre",
    "FR": "Amigo(a)",
    "SU": "Supervisor",
    "MO": "Madre",
    "PA": "Socio",
    "RE": "Recomendación",
    "FY": "Familiar",
    "SI": "Hermana",
    "SP": "Conyuge",
    "OT": "Otro",
}


class RelatedPersons(AbstractModel):
    name = models.CharField(max_length=150)
    related_person_type = models.CharField(
        max_length=2, choices=RELATED_PERSON_TYPE_CHOICES, default="FR"
    )
