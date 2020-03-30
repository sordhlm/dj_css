# Generated by Django 2.2.10 on 2020-03-28 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_contact_teams'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='consumption',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
