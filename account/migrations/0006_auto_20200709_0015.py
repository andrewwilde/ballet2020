# Generated by Django 2.2.9 on 2020-07-09 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200709_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danceclass',
            name='studio',
            field=models.CharField(choices=[('Studio 1', 'Studio 1'), ('Studio 2', 'Studio 2')], max_length=20),
        ),
    ]
