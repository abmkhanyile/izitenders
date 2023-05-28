from django.db import models
from ckeditor.fields import RichTextField

class articles(models.Model):
    title = RichTextField(blank=False)
    articleBody = RichTextField(blank=False)
    publisher = RichTextField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = ('Articles')


