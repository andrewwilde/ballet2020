# Generated by Django 2.2.9 on 2020-07-16 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_danceclass_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(default='Wilde', max_length=30),
            preserve_default=False,
        ),
    ]
