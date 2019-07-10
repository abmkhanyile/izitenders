from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import TenderSearchForm, TestimonialsForm
from contact_us.forms import ContactForm
from packages.models import Packages
from tender_details.models import Tender, Province, Category
from django.http import HttpResponse
from django.core import serializers
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings

# Create your views here.
def homeView(request):
    if request.method == "post":
        tForm = TestimonialsForm(request.POST)

        if tForm.is_valid():
            tForm.save()

            msg = EmailMessage(
                'Testimonial',
                tForm.cleaned_data['message'],
                settings.EMAIL_HOST_USER,
                connection=mail.get_connection(),
            )
            msg.send(fail_silently=True)
            return redirect('/testimonial_done/')
        else:
            return redirect('/')

    else:
        tenders = Tender.objects.all()
        if request.GET.get('province_id') is not None:
            p_id = request.GET.get('province_id')
            prov = Province.objects.get(pk=p_id)
            tenders = prov.tender_set.all()

        if request.GET.get('cat_id') is not None:
            c_id = request.GET.get('cat_id')
            cat = Category.objects.get(pk=c_id)
            tenders = cat.tender_set.all()

        search_form = TenderSearchForm()
        contact_form = ContactForm()
        t_form = TestimonialsForm()
        packages = Packages.objects.all()
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
                                              't_form': t_form,
                                              'bronze': bronze,
                                              'silver': silver,
                                              'gold': gold,
                                              'corporate': corporate,
                                              'tenders': tenders,
                                              'provinces': provinces,
                                              'categories': categories})

#this view displays the number of tenders per province.
def province_view(request, province_pk):
    print(request.path)
    province = Province.objects.get(pk=province_pk)
    tenders = province.tender_set.all()
    data = serializers.serialize('json', tenders, fields=('refNum, summary, siteInspectionDate, closingDate'))
    return HttpResponse(data, content_type='application/json')


def Testimonial_done_view(request):
    return render(request, 'Testimonial_done.html')