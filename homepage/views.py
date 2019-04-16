from django.shortcuts import render
from .forms import TenderSearchForm
from contact_us.forms import ContactForm
from packages.models import Packages
from tender_details.models import Tender, Province, Category

# Create your views here.
def homeView(request):
    search_form = TenderSearchForm()
    contact_form = ContactForm()
    packages = Packages.objects.all()
    tenders = Tender.objects.all()
    provinces = Province.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {"search_form": search_form,
                                          "contact_form": contact_form,
                                          "packages": packages,
                                          "tenders": tenders,
                                          "provinces": provinces,
                                          "categories": categories})