from django.shortcuts import render
from .models import Tender, Category
from .forms import TenderSearchForm, SendEmailForm
from django.contrib import messages
from django.http import HttpResponse
from django.template import Context, Template
from django.core.mail import EmailMessage
from itertools import chain
from django.core import mail
from django.conf import settings


def tenders_list_view(request):
    if request.method == 'POST':
        searchForm = TenderSearchForm(request.POST)
        if searchForm.is_valid():
            searchedText = searchForm.cleaned_data['searchField']
            selectedCat = searchForm.cleaned_data['categorySelectionField']
            selectedProvince = searchForm.cleaned_data['provinceSelectionField']

            # The line below filters the tenders according the the Selected Categories and Provinces...
            preSearchTender = Tender.objects.filter(tenderCategory__in=selectedCat).filter(tenderProvince__in=selectedProvince)

            foundTenders = Tender.objects.none()  # declare an empty queryset for tenders.
            filteredCats = Category.objects.filter(catDescription__icontains=searchedText.strip())
            if filteredCats.exists():
                foundTenders = foundTenders | preSearchTender.filter(tenderCategory__in=filteredCats)
            # The line below splits the search string into substrings for a more accurate search result.
            else:
                sText = searchedText.split()
                if len(sText) == 1:
                    foundTenders = preSearchTender.filter(summary__icontains=sText[0].strip())      #searchs for the given word.
                else:
                    # Searches for the first two words of a given string. they must exist somewhere in the tender summary, the order is not important.
                    foundTenders = preSearchTender.filter(summary__icontains=sText[0].strip()).filter(summary__icontains=sText[1].strip())

            args = {
                'search_form': searchForm,
                'tenders': foundTenders.distinct()
            }
            return render(request, 'tenders.html', args)
    else:
        err_msg = messages.get_messages(request)

        searchForm = TenderSearchForm()
        sendEmail_Form = SendEmailForm()
        tenders = Tender.objects.all()
        args = {'search_form': searchForm,
                'send_email_form': sendEmail_Form,
                'tenders': tenders,
                'messages': err_msg}
        return render(request, 'tenders.html', args)


def send_email_view(request):
    if request.method == 'POST':
        emailForm = SendEmailForm(request.POST)
        if emailForm.is_valid():
            email_addr = emailForm.cleaned_data['email']
            tender_pks = emailForm.cleaned_data['tender_pk']

            container_qs = Tender.objects.none()
            tenderObj_container = list()

            tender_pks_list = tender_pks.split(',')[:-1]
            for tender_pk in tender_pks_list:
                tenderObj = Tender.objects.get(id=int(tender_pk.strip()))
                tenderObj_container.append(tenderObj)

            tender_qs = list(chain(container_qs, tenderObj_container))

            # the actual sending of the email.
            html = Template('<html><head><title>Matched Tenders</title></head><body> {% load tz %}<div style="margin: 20px 5px 15px 20px;"> <table border="1" width="100%"> <thead> <tr><th width="10%">Attachment Name</th> <th width="15%">Tender Ref</th> <th width="45%">Description</th> <th width="15%">Closing Date</th> <th width="15%">Site Inspection Date</th> </tr></thead> <tbody>{% for tender in tenders %} <tr> <td><div style="background-color: yellow;">tender{{ forloop.counter }}</div></td> <td>{{ tender.refNum }}</td> <td>{{ tender.summary|upper }}</td> <td>{{ tender.closingDate }}</td> <td>{{ tender.siteInspectionDate }}</td> </tr> {% endfor %}</tbody> </table> </div></body></html>')
            context = Context({'tenders': tender_qs})
            renderedHtml = html.render(context)

            connection = mail.get_connection()
            emailMsg = EmailMessage(
                'LEADS HUB TENDERS',
                renderedHtml,
                settings.EMAIL_HOST_USER,
                [email_addr],
                reply_to=['info@leadshub.co.za'],
                headers={'Message-ID': 'LH00'},
                connection=connection
            )

            tenderHtml = Template(
                '<html><head> <title>Matched Tender</title></head><body>{% load tz %} <div style="margin: 20px 5px 15px 20px;"> <style> td{padding:10px 5px 10px 0px; border-top: 1px solid #dee2e6; vertical-align:top;} </style> <table> <tbody style="font-size: 14px; font-family: Helvetica;"> <tr> <td style="font-weight: bold; width: 150px;">Tender Details:</td> <td>{{ tender.description|safe }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Tender Documents: </td> <td>{{ tender.tDocLinks|safe }}</td> </tr> </tbody> </table> </div></body></html>')

            for i, tender in enumerate(tender_qs):
                contxt = Context({'tender': tender})
                renderedTenderHtml = tenderHtml.render(contxt)
                emailMsg.attachments.append(('tender{}.html'.format(i + 1), renderedTenderHtml, 'text/html'))

            emailMsg.content_subtype = "html"
            emailMsg.send(fail_silently=False)

            return render(request, 'email_sent_successfully.html')
        else:
            messages.warning(request, "Something went wrong with the sending of the email, please try again.")

            searchForm = TenderSearchForm()
            sendEmail_Form = SendEmailForm()
            tenders = Tender.objects.all()
            args = {'search_form': searchForm,
                    'send_email_form': sendEmail_Form,
                    'tenders': tenders,
                    }
            return render(request, 'tenders.html', args)


