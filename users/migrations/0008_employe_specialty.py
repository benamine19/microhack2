# Generated by Django 5.0.4 on 2024-04-27 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_employe_speciality_employe_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='specialty',
            field=models.CharField(default='General', max_length=50),
        ),
    ]