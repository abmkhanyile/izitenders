from django.db import models
from tender_details.models import Keywords

class Generic_cats(models.Model):
    cat_code = models.CharField(max_length=10)
    cat_description = models.CharField(max_length=450, blank=True, null=True)
    cat_kw = models.ManyToManyField(Keywords, blank=True)

    def __str__(self):
        return self.cat_description
