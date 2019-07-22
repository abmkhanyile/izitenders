from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from .forms import ContactForm

def contact_us_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            surname = contact_form.cleaned_data['surname']
            email = contact_form.cleaned_data['email']
            contact_num = contact_form.cleaned_data['contact_num']
            message = contact_form.cleaned_data['message']
            try:
                send_mail('Website Enquiry', message+'\n\n'+name+' '+surname+'\n'+contact_num+'\n'+email, settings.EMAIL_HOST_USER, ['leadshub.co@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'email_sent_success.html')
        return render(request, "contact_us.html", {'contact_form': contact_form})
    else:
        contact_form = ContactForm()
        return render(request, 'contact_us.html', {'contact_form': contact_form})


def email_success_view(request):
    return render(request, 'email_sent_success.html')
