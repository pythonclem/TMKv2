# Generated by Django 5.0.3 on 2024-03-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsdb', '0004_standing'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='postponed',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='status',
            field=models.CharField(max_length=255, null=True),
        ),
    ]