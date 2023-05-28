from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone


#Stores the categories.
class Category(models.Model):
    catDescription = models.CharField(max_length=100)
    topCat = models.BooleanField(default=False)
    topCat_id = models.IntegerField(default=0)

    @property
    def get_num_of_assigned_tender(self):
        return self.tender_set.all().count()

    class Meta:
        verbose_name_plural = ('Categories')

    def __str__(self):
        return self.catDescription


#The provinces model stores the Provinces
class Province(models.Model):
    province_name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.province_name



# This models stores the keywords in the database.
class Keywords(models.Model):
    keyword = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = ('Keywords')
        ordering = ['keyword', ]

    def __str__(self):
        return self.keyword



#This is the model that stores the tender.
class Tender(models.Model):
    tenderCategory = models.ManyToManyField(Category, blank=False)       #this field holds the tender category, e.g. construction, engineering, human resources etc.
    tenderProvince = models.ManyToManyField(Province, blank=False)       #this is the province the tender was advertised from.
    buyersName = models.CharField(max_length=100, blank=True, null=True)   #this is the name of the Buyer e.g. Dept. of Transport, Transnet, Dept of Agriculture etc.
    summary = models.TextField(blank=False)      #this is the tender title as per the Buyer.
    refNum = models.CharField(max_length=100)    #tender ref number as per the Buyer.
    issueDate = models.DateTimeField(blank=True, null=True)     #date the tender was published
    closingDate = models.DateTimeField(default=timezone.now, blank=True, null=True)   #tender closing date
    siteInspectionDate = models.DateTimeField(blank=True, null=True)
    siteInspection = RichTextField(blank=True, null=True)     #site inspection date, if any
    enquiries = RichTextField(blank=True, null=True) #this field stores details of the contact person, for the tender.
    description = RichTextField(blank=True, null=True)   #this is the body of the tender. the tender details are captured here.
    assigned_keywords = models.ManyToManyField(Keywords, blank=True)
    matched = models.BooleanField(default=False, blank=False)
    capture_date = models.DateField(default=timezone.now, blank=False, null=False)
    date_assigned = models.DateField(blank=True, null=True)
    kw_assigned = models.BooleanField(default=False, blank=True)
    tDocLinks = RichTextField(blank=True)
    pdfType = models.BooleanField(default=False, blank=False)
    pdfLink = models.TextField(blank=True)

    def check_if_expired(self):
        if self.closingDate != None:
            if self.closingDate < timezone.now():
                return True
            else:
                return False
        else:
            return False

    def check_docs(self):
        if self.tDocLinks != None:
            return True
        else:
            return False

    class Meta:
        ordering = ['-closingDate']






