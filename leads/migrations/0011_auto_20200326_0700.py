# Generated by Django 2.2.10 on 2020-03-26 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_lead_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='source',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Source of Lead'),
        ),
    ]
