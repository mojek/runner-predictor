# Generated by Django 2.2.1 on 2019-05-22 10:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_runner_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='runner',
            name='birth_year',
            field=models.PositiveIntegerField(default=1910, validators=[django.core.validators.MinValueValidator(1910)]),
            preserve_default=False,
        ),
    ]