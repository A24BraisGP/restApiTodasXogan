# Generated by Django 5.2.1 on 2025-06-03 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoxogo',
            name='desarrolladora',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
