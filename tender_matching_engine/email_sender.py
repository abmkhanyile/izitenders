from django.core import mail
from django.core.mail import EmailMessage
from user_accounts.models import CompanyProfile, UsersTenders
from django.utils import timezone
from django.shortcuts import render
from django.template import Context, Template
from django.conf import settings

def compile_tenders():
    #pulls the user objects, from which to pull the matched tenders for the day.
    users = CompanyProfile.objects.all()

    #iterate over the users list and check if they have tenders assigned to them for the day.
    for user in users:
        if user.user.is_active:
            if user.commencementDate.date() == timezone.now().date():
                # filters all the tenders with a closing date in the future regardless of when the tender was assigned
                # this caters for new users who just signed up. This allows them to get all the open tenders they are interested in.
                daily_tenders = user.assignedTenders.filter(closingDate__gte=timezone.now())
                send_email(user, daily_tenders)
            else:
                # filters all the tenders with the assigned_date of today and a closing date in the future.
                daily_tenders = user.assignedTenders.filter(userTenderLink__sent=False, closingDate__gte=timezone.now())
                send_email(user, daily_tenders)
        else:
            print('{} is inactive.'.format(user.user.username))


def send_email(user, dTenders):

    delivery_emails = user.deliveryEmails.split(',')

    if len(dTenders) > 0:
        html = Template('<html><head><title>Matched Tenders</title></head><body> {% load tz %}<div style="margin: 20px 5px 15px 20px;"> <table border="1" width="100%"> <thead> <tr><th width="10%">Attachment Name</th> <th width="15%">Tender Ref</th> <th width="45%">Description</th> <th width="15%">Closing Date</th> <th width="15%">Site Inspection Date</th> </tr></thead> <tbody>{% for tender in tenders %} <tr> <td><div style="background-color: yellow;">tender{{ forloop.counter }}</div></td> <td>{{ tender.refNum }}</td> <td>{{ tender.summary|upper }}</td> <td>{{ tender.closingDate }}</td> <td>{{ tender.siteInspectionDate }}</td> </tr> {% endfor %}</tbody> </table> </div></body></html>')
        context = Context({'tenders': dTenders})
        renderedHtml = html.render(context)

        connection = mail.get_connection()
        emailMsg = EmailMessage(
            'LEADS HUB - DAILY TENDERS',
            renderedHtml,
            settings.EMAIL_HOST_USER,
            delivery_emails,
            reply_to=['info@leadshub.co.za'],
            headers={'Message-ID': 'LH00'},
            connection=connection
        )

        tenderHtml = Template('<html><head> <title>Matched Tender</title></head><body>{% load tz %} <div style="margin: 20px 5px 15px 20px;"> <style> td{padding:10px 5px 10px 0px; border-top: 1px solid #dee2e6; vertical-align:top;} </style> <table> <tbody style="font-size: 14px; font-family: Helvetica;"> <tr> <td style="font-weight: bold; width: 150px;">Tender Details:</td> <td>{{ tender.description|safe }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Tender Documents: </td> <td>{{ tender.tDocLinks|safe }}</td> </tr> </tbody> </table> </div></body></html>')

        for i, tender in enumerate(dTenders):
            contxt = Context({'tender': tender})
            renderedTenderHtml = tenderHtml.render(contxt)
            emailMsg.attachments.append(('tender{}.html'.format(i+1), renderedTenderHtml, 'text/html'))
            UserTenderObj = UsersTenders.objects.get(user=user, tender=tender)
            if UserTenderObj.sent == False:
                UserTenderObj.sent = True
                UserTenderObj.save()

        emailMsg.content_subtype = "html"
        emailMsg.send(fail_silently=False)

# connection = mail.get_connection()   # Use default email connection
# messages = compile_emails()
# connection.send_messages(messages)