# Generated by Django 2.2 on 2019-05-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='packages',
            name='package_id',
            field=models.IntegerField(default=0),
        ),
    ]
