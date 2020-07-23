# Generated by Django 2.2.9 on 2020-07-09 00:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_student_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='danceclass',
            name='date_time',
        ),
        migrations.AddField(
            model_name='danceclass',
            name='day',
            field=models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], default='Monday', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='danceclass',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='danceclass',
            name='stop_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]