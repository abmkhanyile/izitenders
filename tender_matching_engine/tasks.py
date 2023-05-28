from __future__ import absolute_import, unicode_literals
from celery import shared_task
from tender_details.models import Tender
from django.core import mail
from django.core.mail import EmailMessage
from user_accounts.models import CompanyProfile, UsersTenders
from django.utils import timezone
from django.shortcuts import render
from django.template import Context, Template


# the task below handles the matching of tenders.
@shared_task
class MatchingTool:
    # This function searches the keywords table in the db if
    # they match the assigned keywordTags to the tenders.
    def matchTendersToUser(self):
        # section below pulls all assigned keywords to the tenders as per the
        # keywordTags field in the tenders db table.
        unmatchedTenders = Tender.objects.all()
        users = CompanyProfile.objects.all()

        for tenderObj in unmatchedTenders:
            tender_provinces = tenderObj.tenderProvince.all()
            tenderKeywords = tenderObj.assigned_keywords.all()

            for user in users:
                userProvinces = user.provinces.all()
                userKeywords = user.keywords.all()

                matchedProvinces = tender_provinces.intersection(userProvinces)
                matchedKeywords = tenderKeywords.intersection(userKeywords)

                if len(matchedProvinces) > 0:
                    if len(matchedKeywords) > 0:
                        UsersTenders.objects.create(user=user, tender=tenderObj)
                        if tenderObj.matched == False:
                            tenderObj.matched = True
                            tenderObj.date_assigned = timezone.now()
                            tenderObj.save()






# the task below handles the sending of emails to clients
@shared_task
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
        html = Template('<html><head> <title>Matched Tenders</title></head><body> <div style="margin: 20px 5px 15px 20px;"> {% load tz %} <table> {% for tender in tenders %} <tr> <td>tender{{ forloop.counter }}</td> <td>{{ tender.refNum }}</td> <td>{{ tender.summary|upper }}</td> <td>{{ tender.closingDate }}</td> <td>{{ tender.siteInspectionDate }}</td> </tr> {% endfor %} </table> </div></body></html>')
        context = Context({'tenders': dTenders})
        renderedHtml = html.render(context)

        connection = mail.get_connection()
        emailMsg = EmailMessage(
            renderedHtml,
            delivery_emails,
            reply_to=['admin@leadshub.co.za'],
            headers={'Message-ID': 'foo'},
            connection=connection
        )

        tenderHtml = Template('<html><head> <title>Matched Tender</title></head><body><div style="margin: 20px 5px 15px 20px;">{% load tz %} <table> <tbody style="font-size: 14px; font-family: Helvetica;"> <tr> <td style="font-weight: bold; width: 150px;">Tender Ref:</td> <td>{{ tender.refNum }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Summary:</td> <td><p>{{ tender.summary|upper|safe }}</p></td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Buyer:</td> <td>{{ tender.buyersName|upper }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Date Published: </td> <td>{{ tender.issueDate|date }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px; font-color: red;"> Closing Date: </td> <td style="color: #ff0000;">{{ tender.closingDate|localtime }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Site Inspection: </td> <td>{{ tender.siteInspection|safe }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Enquiries:</td> <td>{{ tender.enquiries|safe }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Description:</td> <td>{{ tender.description|safe }}</td> </tr> <tr> <td style="font-weight: bold; width: 150px;">Tender Documents: </td> <td>{{ tender.tDocLinks|safe }}</td> </tr> </tbody> </table></div></body></html>')

        for i, tender in enumerate(dTenders):
            contxt = Context({'tender': tender})
            renderedTenderHtml = tenderHtml.render(contxt)
            emailMsg.attach('tender{}'.format(i), renderedTenderHtml, 'text/html')
            print(user.user_id)
            # print(tender)
            UserTenderObj = UsersTenders.objects.get(user=user, tender=tender)
            print(UserTenderObj.tender.summary)
            UserTenderObj.sent = True
            UserTenderObj.save()

        emailMsg.send(fail_silently=False)



