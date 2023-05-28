from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from tender_details.models import Keywords, Category, Province, Tender
from packages.models import Packages
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from ckeditor.fields import RichTextField
from decimal import *


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    accountNumber = models.CharField(max_length=25, default=1, blank=False, null=False)
    companyName = models.CharField(max_length=200, blank=False)
    companyRegNum = models.CharField(max_length=30, blank=True)
    contactNumber = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=300, blank=True)
    areaCode = models.CharField(max_length=10, blank=False)
    deliveryEmails = models.TextField(
        blank=True)  # this is the list of all the people chosen to recieve daily notification.
    tenderCategory = models.ManyToManyField(Category, blank=False)  # links the user to the chosen category.
    provinces = models.ManyToManyField(Province, blank=False)  # links the user to the chosen Provinces.
    package = models.ForeignKey(Packages, default=1, blank=False,
                                on_delete=models.PROTECT)  # links the user to the chosen package.
    assignedTenders = models.ManyToManyField(Tender, through='UsersTenders',
                                             related_name='UserCompanies')  # creates a connection between the user and the assigned tenders to the user.
    pymntMethod = models.IntegerField(blank=True,
                                      default=3)  # this is the chosen payment method (e.g credit card=1, debit order=2 or direct debit=3)
    keywords = models.ManyToManyField(Keywords)  # links the user to the chosen keywords.
    extraKeywords = models.TextField(default='',
                                     blank=True)  # this field acts as a container of extra keywords from the user. These are keywords that we do not have in our database.
    contractDuration = models.IntegerField(blank=False, default=12)
    termsAndConditions = models.BooleanField(blank=False,
                                             default=1)  # this is the T&C's field that must be agreed to by the client.
    commencementDate = models.DateTimeField(default=timezone.now, blank=True)
    kw_chosen = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.companyName

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})

    def check_for_kw(self):
        if len(self.keywords.all()) > 0:
            return 1
        else:
            return 0


def create_company_profile(sender, **kwargs):
    if kwargs['created']:
        CompanyProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_company_profile, sender=User, dispatch_uid="my_unique_identifier")


class Banking_Details(models.Model):
    CHOICES = (('CHEQUE', 'CHEQUE'),
               ('SAVINGS', 'SAVINGS'),
               ('TRANSMISSION', 'TRANSMISSION'),
               ('CURRENT', 'CURRENT'),
               )
    user_CompanyProfile = models.OneToOneField(CompanyProfile, on_delete=models.CASCADE, primary_key=True)
    accHolder = models.CharField(max_length=150, blank=False)
    bankName = models.CharField(max_length=100, blank=False)
    accNum = models.CharField(max_length=30, blank=False)
    accType = models.CharField(max_length=30, blank=False, choices=CHOICES)
    branchName = models.CharField(max_length=150, blank=True)
    branchCode = models.CharField(max_length=10, blank=False)

    class Meta:
        verbose_name_plural = ('Banking details')


# def create_bankingDetails(sender, **kwargs):
#     if kwargs['created']:
#         Banking_Details.objects.create(user_CompanyProfile=kwargs['instance'])
# post_save.connect(create_bankingDetails, sender=CompanyProfile)


class Notes(models.Model):
    noteText = RichTextField(blank=False)
    company = models.ForeignKey(CompanyProfile, blank=False, on_delete=models.CASCADE, null=True)
    captured_by = models.CharField(max_length=150, blank=False)
    date_captured = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        verbose_name_plural = ('Notes')


class OurDetails(models.Model):
    compName = models.CharField(max_length=250, blank=False)
    compRegNum = models.CharField(max_length=30)
    VAT_num = models.CharField(max_length=25)
    contactNumber = models.CharField(max_length=30, blank=True)
    faxNumber = models.CharField(max_length=30, blank=True)
    emailAddress = models.CharField(max_length=150, blank=False)
    website = models.CharField(max_length=150, blank=True)
    physicalAddress = RichTextField(blank=True)
    postalAddress = RichTextField(blank=True)
    bankName = models.CharField(max_length=100, blank=False)
    bankAccNum = models.CharField(max_length=30, blank=False)
    accType = models.CharField(max_length=30)
    branchName = models.CharField(max_length=50)
    branchCode = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = ('Our Details')


# This models holds the transactions for the clients.
class Invoice_Items(models.Model):
    date_item_created = models.DateTimeField(default=timezone.now, blank=False)
    item_description = models.CharField(max_length=250, blank=False)
    amount = models.DecimalField(max_digits=30, decimal_places=2, blank=False)

    class Meta:
        verbose_name_plural = ('Invoice Items')

    def __str__(self):
        return self.item_description


# This model holds client invoices.
class Invoices(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, blank=False)
    invoiceNumber = models.CharField(max_length=50, blank=False)
    invoiceDate = models.DateTimeField(default=timezone.now, blank=False)
    VAT_percentage = models.IntegerField(default=15, blank=False)
    package = models.ForeignKey(Packages, blank=False, on_delete=models.CASCADE, null=True)
    pymnt_status = models.BooleanField(default=False, blank=False)

    def total(self):
        tot = Decimal(0.00).quantize(Decimal('0.00'))
        tot = Decimal(tot + self.package.price * self.company.contractDuration).quantize(Decimal('0.00'))
        return tot

    def due_date(self):
        return self.invoiceDate + timedelta(days=7)

    class Meta:
        verbose_name_plural = ('Invoices')


# connects users to the tenders they match.
class UsersTenders(models.Model):
    user = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='userTenderLink')
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='userTenderLink')
    sent = models.BooleanField(default=False, blank=False)


class Assignedtenders(models.Model):
    companyprofile = models.ForeignKey(CompanyProfile, models.DO_NOTHING)
    tender = models.ForeignKey(Tender, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_account_companyprofile_assignedTenders'
        unique_together = (('companyprofile', 'tender'),)











