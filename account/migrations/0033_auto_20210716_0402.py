# Generated by Django 2.2.9 on 2021-07-16 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_auto_20210716_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danceclass',
            name='price_id',
            field=models.CharField(choices=[('price_1HRWnQIQ4hPK7zxOAOwjHQvv', 'Pre Creative Dance'), ('price_1HRWn3IQ4hPK7zxOb64qqBCG', 'Kinder Tap'), ('price_1HRWmmIQ4hPK7zxOQ8GKSplt', 'Intermediate Jazz'), ('price_1HmWiPIQ4hPK7zxOxdtqzmtJ', 'Kinder Jazz'), ('price_1HRWmYIQ4hPK7zxOEcN1irzM', 'Beginning 1 Jazz'), ('price_1HRWm7IQ4hPK7zxOh8w1Ksqy', 'Beginning 2 Ballet'), ('price_1HRWlgIQ4hPK7zxO3I0rUBCQ', 'Beginning 1 Ballet'), ('price_1HRWjxIQ4hPK7zxOxZKgZTg1', 'Pre Ballet'), ('price_1HRWHPIQ4hPK7zxOW0DfgEpX', 'Kinder Ballet'), ('price_1J6kdfIQ4hPK7zxOh2FE3CTf', 'Kinder Creative'), ('price_1J6kbVIQ4hPK7zxOznHaUB64', 'Beginning 1 Tap'), ('price_1J6kc3IQ4hPK7zxObM24WnNy', 'Beginning 1 Jazz'), ('price_1J6kcTIQ4hPK7zxOFBmLXE6J', 'Intermediate 1 Ballet'), ('price_1J6kcjIQ4hPK7zxOR8j6s6b4', 'Beginning 2 Jazz'), ('price_1JDgu9IQ4hPK7zxO2H2lXUfV', 'Mom & Tots Creative Dance'), ('price_1JDiELIQ4hPK7zxOlBF0gU8E', 'Beginning 1 Creative Dance')], default='', max_length=50),
        ),
    ]
