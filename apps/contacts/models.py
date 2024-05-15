from django.db import models

from apps.abstracts.models import AbstractModel
from apps.address.models import Address
from apps.emails.models import Emails
from apps.important_dates.models import ImportantDates
from apps.phones.models import Phones
from apps.related_persons.models import RelatedPersons
from apps.tags.models import Tags
from apps.users.models import User

# Create your models here.


class Contacts(AbstractModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    last_nmae = models.CharField(max_length=50, blank=False, null=False)
    company = models.CharField(max_length=50, blank=True, null=True)
    phones = models.ManyToManyField(Phones, blank=False)
    emails = models.ManyToManyField(Emails, blank=True)
    address = models.ManyToManyField(Address, blank=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    important_dates = models.ManyToManyField(ImportantDates, blank=True)
    related_persons = models.ManyToManyField(RelatedPersons, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    sip = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=250, blank=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True)
