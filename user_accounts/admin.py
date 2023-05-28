from django.contrib import admin
from .models import CompanyProfile, Banking_Details, Notes, OurDetails, Invoices, Invoice_Items


admin.site.site_header = 'LeadsHub Admin'

@admin.register(CompanyProfile)
class Company_Profile_Admin(admin.ModelAdmin):
    list_display = ['companyName', 'companyRegNum', 'contactNumber']
    fields = ('user', 'companyName', 'companyRegNum',
              'contactNumber', 'address', 'areaCode', 'deliveryEmails',
              'tenderCategory', 'provinces', 'package', 'pymntMethod',
              'keywords', 'extraKeywords', 'contractDuration',
              'termsAndConditions', 'commencementDate')
    raw_id_fields = ('keywords',)
    filter_horizontal = ('tenderCategory', 'provinces')
    search_fields = ['accountNumber', 'contactNumber']

@admin.register(Banking_Details)
class Banking_Details_Admin(admin.ModelAdmin):
    list_display = ['user_CompanyProfile', 'accHolder', 'bankName', 'accNum']


@admin.register(Notes)
class Notes_Admin(admin.ModelAdmin):
    list_display = ['date_captured', 'company', 'noteText', 'captured_by']

@admin.register(OurDetails)
class OurDetails_Admin(admin.ModelAdmin):
    list_display = ['compName', 'compRegNum', 'VAT_num', 'contactNumber', 'faxNumber', 'emailAddress', 'physicalAddress',
                    'postalAddress', 'bankName', 'bankAccNum', 'accType', 'branchName', 'branchCode']


@admin.register(Invoices)
class Invoices_Admin(admin.ModelAdmin):
    list_display = ['company', 'invoiceNumber', 'invoiceDate', 'VAT_percentage']


@admin.register(Invoice_Items)
class Invoice_Items_Admin(admin.ModelAdmin):
    list_display = ['date_item_created', 'item_description', 'amount']

