# Generated by Django 2.2.9 on 2020-08-21 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_auto_20200723_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='danceclass',
            name='secondary_image',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]