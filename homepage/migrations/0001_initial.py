# Generated by Django 2.2 on 2019-07-10 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('companyName', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=100)),
                ('displayed', models.BooleanField(default=False)),
            ],
        ),
    ]
