# Generated by Django 4.0.2 on 2022-02-18 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SellHub', '0028_alter_profiluzytkownika_ulubione_ogloszenia'),
    ]

    operations = [
        migrations.AddField(
            model_name='ogloszenie',
            name='wyswietlenia',
            field=models.IntegerField(default=0),
        ),
    ]
