# Generated by Django 4.0.2 on 2022-02-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SellHub', '0025_alter_ogloszenie_przebieg'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiluzytkownika',
            name='ulubione_ogloszenia',
            field=models.ManyToManyField(to='SellHub.Ogloszenie'),
        ),
    ]