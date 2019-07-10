from django.db import models

class Testimonials(models.Model):
    fname = models.CharField(max_length=100, blank=False)
    lname = models.CharField(max_length=100, blank=False)
    designation = models.CharField(max_length=100, blank=False)
    companyName = models.CharField(max_length=100, blank=False)
    message = models.TextField(max_length=100, blank=False)
    displayed = models.BooleanField(default=False)
