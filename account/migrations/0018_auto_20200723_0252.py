# Generated by Django 2.2.9 on 2020-07-23 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20200721_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='danceclass',
            name='payment_frequency',
            field=models.CharField(choices=[('each month', 'each month'), ('one-time payment', 'one-time payment')], default='each month', max_length=20),
        ),
        migrations.AlterField(
            model_name='danceclass',
            name='curriculum',
            field=models.FilePathField(blank=True, null=True, path='/home/andrew/projects/ballet2020/staging/front/static/docs'),
        ),
    ]
