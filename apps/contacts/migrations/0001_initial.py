# Generated by Django 5.0.4 on 2024-05-15 16:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        ('emails', '0001_initial'),
        ('important_dates', '0001_initial'),
        ('phones', '0001_initial'),
        ('related_persons', '0001_initial'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('company', models.CharField(blank=True, max_length=50, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('sip', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.ManyToManyField(blank=True, to='address.address')),
                ('emails', models.ManyToManyField(blank=True, to='emails.emails')),
                ('important_dates', models.ManyToManyField(blank=True, to='important_dates.importantdates')),
                ('phones', models.ManyToManyField(to='phones.phones')),
                ('related_persons', models.ManyToManyField(blank=True, to='related_persons.relatedpersons')),
                ('tags', models.ManyToManyField(blank=True, to='tags.tags')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
