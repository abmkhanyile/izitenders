# Generated by Django 2.1.2 on 2019-04-09 15:02

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tender_details', '0001_initial'),
        ('packages', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignedtenders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'user_account_companyprofile_assignedTenders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('accountNumber', models.CharField(default=1, max_length=25)),
                ('companyName', models.CharField(max_length=200)),
                ('companyRegNum', models.CharField(blank=True, max_length=30)),
                ('contactNumber', models.CharField(max_length=20)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('areaCode', models.CharField(max_length=10)),
                ('deliveryEmails', models.TextField(blank=True)),
                ('pymntMethod', models.IntegerField(blank=True, default=3)),
                ('extraKeywords', models.TextField(blank=True, default='')),
                ('contractDuration', models.IntegerField(default=12)),
                ('termsAndConditions', models.BooleanField(default=1)),
                ('commencementDate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_item_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('item_description', models.CharField(max_length=250)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=30)),
            ],
            options={
                'verbose_name_plural': 'Invoice Items',
            },
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoiceNumber', models.CharField(max_length=50)),
                ('invoiceDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('VAT_percentage', models.IntegerField(default=15)),
            ],
            options={
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noteText', ckeditor.fields.RichTextField()),
                ('captured_by', models.CharField(max_length=150)),
                ('date_captured', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Notes',
            },
        ),
        migrations.CreateModel(
            name='OurDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compName', models.CharField(max_length=250)),
                ('compRegNum', models.CharField(max_length=30)),
                ('VAT_num', models.CharField(max_length=25)),
                ('contactNumber', models.CharField(blank=True, max_length=30)),
                ('faxNumber', models.CharField(blank=True, max_length=30)),
                ('emailAddress', models.CharField(max_length=150)),
                ('physicalAddress', ckeditor.fields.RichTextField(blank=True)),
                ('postalAddress', ckeditor.fields.RichTextField(blank=True)),
                ('bankName', models.CharField(max_length=100)),
                ('bankAccNum', models.CharField(max_length=30)),
                ('accType', models.CharField(max_length=30)),
                ('branchName', models.CharField(max_length=50)),
                ('branchCode', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Our Details',
            },
        ),
        migrations.CreateModel(
            name='UsersTenders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.BooleanField(default=False)),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTenderLink', to='tender_details.Tender')),
            ],
        ),
        migrations.CreateModel(
            name='Banking_Details',
            fields=[
                ('user_CompanyProfile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_accounts.CompanyProfile')),
                ('accHolder', models.CharField(max_length=150)),
                ('bankName', models.CharField(max_length=100)),
                ('accNum', models.CharField(max_length=30)),
                ('accType', models.CharField(choices=[('CHEQUE', 'CHEQUE'), ('SAVINGS', 'SAVINGS'), ('TRANSMISSION', 'TRANSMISSION'), ('CURRENT', 'CURRENT')], max_length=30)),
                ('branchName', models.CharField(blank=True, max_length=150)),
                ('branchCode', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Banking details',
            },
        ),
        migrations.AddField(
            model_name='userstenders',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTenderLink', to='user_accounts.CompanyProfile'),
        ),
        migrations.AddField(
            model_name='notes',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_accounts.CompanyProfile'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_accounts.CompanyProfile'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='invoiceItems',
            field=models.ManyToManyField(blank=True, to='user_accounts.Invoice_Items'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='assignedTenders',
            field=models.ManyToManyField(related_name='UserCompanies', through='user_accounts.UsersTenders', to='tender_details.Tender'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='keywords',
            field=models.ManyToManyField(to='tender_details.Keywords'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='package',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='packages.Packages'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='provinces',
            field=models.ManyToManyField(to='tender_details.Province'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='tenderCategory',
            field=models.ManyToManyField(to='tender_details.Category'),
        ),
    ]
