from django.db import models

class Packages(models.Model):
    package = models.CharField(max_length=20, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    package_id = models.IntegerField(default=0, blank=False)

    @property
    def annualPrice(self):
        return self.price*12

    @property
    def sixMonthPrice(self):
        return self.price*6

    class Meta:
        verbose_name_plural = ('Packages')

    def __str__(self):
        return self.package


