from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def send_marketing_emails():

    unsub_list = []

    with open('C:/PROJECTS/tenderwiz/tender_matching_engine/Utilities/unsubscribe_list.txt', 'r') as uns_file:
        for line in uns_file:
            unsub_list.append(line.strip())

    with open('C:/PROJECTS/tenderwiz/tender_matching_engine/Utilities/email_template2.txt', 'r') as f:
        renderedHtml = f.read()

        email_list = []

        with open('C:/PROJECTS/tenderwiz/tender_matching_engine/Utilities/mailing_list.txt', 'r') as f2:
            for line in f2:
                email_addr = line.strip()
                valid_email = True
                try:
                    validate_email(email_addr)
                    valid_email = True
                except ValidationError:
                    valid_email = False

                if "@sap.com" in email_addr or valid_email == False:
                    continue
                elif email_addr in unsub_list:
                    continue
                else:
                    email_list.append(email_addr)

        connection = mail.get_connection()
        emailMsg = EmailMessage(
            'LEADS AND TENDERS',
            renderedHtml,
            settings.EMAIL_HOST_USER,
            ['ayatech.co@gmail.com'],
            # email_list,
            [],
            reply_to=['info@leadshub.co.za'],
            headers={'Message-ID': 'LH00'},
            connection=connection
        )
        emailMsg.content_subtype = "html"
        emailMsg.send(fail_silently=True)