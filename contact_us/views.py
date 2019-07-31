from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from .forms import ContactForm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def contact_us_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            surname = contact_form.cleaned_data['surname']
            email = contact_form.cleaned_data['email']
            contact_num = contact_form.cleaned_data['contact_num']
            message = contact_form.cleaned_data['message']

            username = settings.EMAIL_HOST_USER
            password = settings.EMAIL_HOST_PASSWORD

            try:

                msg = MIMEMultipart()

                msg['From'] = email
                msg['To'] = 'leadshub.co@gmail.com'
                msg['Subject'] = 'Website Enquiry'
                msg.attach(MIMEText(message+'\n\n'+name+' '+surname+'\n'+contact_num+'\n'+email))

                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(username, password)
                server.sendmail(email, 'leadshub.co@gmail.com', msg.as_string())
                server.quit()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'email_sent_success.html')
        return render(request, "contact_us.html", {'contact_form': contact_form})
    else:
        contact_form = ContactForm()
        return render(request, 'contact_us.html', {'contact_form': contact_form})


def email_success_view(request):
    return render(request, 'email_sent_success.html')


