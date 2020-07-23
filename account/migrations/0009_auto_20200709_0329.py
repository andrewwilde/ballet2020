# Generated by Django 2.2.9 on 2020-07-09 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_danceclass_teacher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminaccount',
            options={'verbose_name': 'Admin', 'verbose_name_plural': 'Admins'},
        ),
        migrations.AlterModelOptions(
            name='danceclass',
            options={'verbose_name': 'Class', 'verbose_name_plural': 'Classes'},
        ),
        migrations.AlterModelOptions(
            name='parentaccount',
            options={'verbose_name': 'Parent', 'verbose_name_plural': 'Parents'},
        ),
        migrations.AlterModelOptions(
            name='teacheraccount',
            options={'verbose_name': 'Teacher', 'verbose_name_plural': 'Teachers'},
        ),
        migrations.AddField(
            model_name='account',
            name='image',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
