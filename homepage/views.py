from django.shortcuts import render
from django.urls import reverse, reverse_lazy
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

    bronze = None
    silver = None
    gold = None
    corporate = None

    for package in packages:
        if package.package_id == 0:
            bronze = package
        elif package.package_id == 1:
            silver = package
        elif package.package_id == 2:
            gold = package
        elif package.package_id == 3:
            corporate = package

    return render(request, 'index.html', {'search_form': search_form,
                                          'contact_form': contact_form,
                                          'bronze': bronze,
                                          'silver': silver,
                                          'gold': gold,
                                          'corporate': corporate,
                                          'tenders': tenders,
                                          'provinces': provinces,
                                          'categories': categories})