# Generated by Django 5.1.3 on 2024-11-17 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_remove_customerprofile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
