# Generated by Django 2.2.1 on 2019-05-06 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('start_date', models.DateField()),
                ('distance', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('elevation_gain', models.PositiveIntegerField(blank=True, null=True)),
                ('elevation_lost', models.PositiveIntegerField(blank=True, null=True)),
                ('itra', models.PositiveIntegerField(blank=True, null=True)),
                ('food_point', models.PositiveIntegerField(blank=True, null=True)),
                ('time_limit', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
            ],
            options={
                'verbose_name_plural': 'races',
                'ordering': ['-start_date'],
                'unique_together': {('name', 'start_date')},
            },
        ),
    ]