# Generated by Django 2.2.28 on 2024-03-21 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0046_auto_20230915_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='danceclass',
            name='sale_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='danceclass',
            name='curriculum',
            field=models.FilePathField(blank=True, null=True, path='/home/andrew/projects/ballet2020/staging/front/static/docs'),
        ),
        migrations.AlterField(
            model_name='danceclass',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Full', 'Class is Full'), ('Closed for Season', 'Closed for Season')], default='Inactive', max_length=20),
        ),
    ]