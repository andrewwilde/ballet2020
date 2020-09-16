# Generated by Django 2.2.9 on 2020-09-16 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_danceclass_secondary_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='danceclass',
            name='price_id',
            field=models.CharField(choices=[('Pre Creative Dance', 'price_1HRWnQIQ4hPK7zxOAOwjHQvv'), ('Kinder Tap', 'price_1HRWn3IQ4hPK7zxOb64qqBCG'), ('Intermediate Jazz', 'price_1HRWmmIQ4hPK7zxOQ8GKSplt'), ('Beginning 1 Jazz', 'price_1HRWmYIQ4hPK7zxOEcN1irzM'), ('Beginning 2 Ballet', 'price_1HRWm7IQ4hPK7zxOh8w1Ksqy'), ('Beginning 1 Ballet', 'price_1HRWlgIQ4hPK7zxO3I0rUBCQ'), ('Pre Ballet', 'price_1HRWjxIQ4hPK7zxOxZKgZTg1'), ('Kinder Ballet', 'price_1HRWHPIQ4hPK7zxOW0DfgEpX')], default='', max_length=50),
        ),
    ]