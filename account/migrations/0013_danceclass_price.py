# Generated by Django 2.2.9 on 2020-07-13 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20200713_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='danceclass',
            name='price',
            field=models.IntegerField(default=35),
            preserve_default=False,
        ),
    ]
