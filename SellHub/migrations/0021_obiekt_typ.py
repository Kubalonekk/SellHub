# Generated by Django 4.0.2 on 2022-02-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SellHub', '0020_obiekt'),
    ]

    operations = [
        migrations.AddField(
            model_name='obiekt',
            name='typ',
            field=models.BooleanField(default=False),
        ),
    ]
