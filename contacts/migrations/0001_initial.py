# Generated by Django 2.2.10 on 2020-07-24 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True, verbose_name='name')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('is_active', models.BooleanField(default=False)),
                ('remain', models.FloatField(blank=True, default=0)),
                ('total', models.FloatField(blank=True, default=0)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adress_contacts', to='common.Address')),
                ('assigned_to', models.ManyToManyField(related_name='contact_assigned_users', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_created_by', to=settings.AUTH_USER_MODEL)),
                ('teams', models.ManyToManyField(related_name='contact_teams', to='teams.Teams')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
