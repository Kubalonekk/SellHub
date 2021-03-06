# Generated by Django 4.0.2 on 2022-02-08 13:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SellHub', '0017_ogloszenie_data_dodania_alter_ogloszenie_nadwozie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiluzytkownika',
            name='numer_telefonu',
            field=models.CharField(max_length=60, null=True, validators=[django.core.validators.RegexValidator(message='Numer telefonu musi zaczynac od +48 i mieć 9 cyfr', regex='^[+](48)\\d{9}$')]),
        ),
    ]
