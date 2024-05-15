# Generated by Django 5.0.4 on 2024-05-15 16:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantDates',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('important_date', models.DateField()),
                ('important_date_type', models.CharField(choices=[('BI', 'Cumpleaños'), ('AN', 'Aniversario'), ('OT', 'Otro')], default='BI', max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
