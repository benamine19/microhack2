# Generated by Django 5.0.4 on 2024-04-27 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_employe_rank_alter_taskresponse_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='speciality',
            field=models.CharField(default='masson', max_length=50),
        ),
        migrations.AddField(
            model_name='employe',
            name='status',
            field=models.CharField(default='available', max_length=50),
        ),
    ]
