from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import re
from smart_open import smart_open
from django.conf import settings
import io
import boto3
from tender_details.models import Tender, Category, Province
import pytz
import random
from .models import Generic_cats
from tender_details.models import Keywords, Category, Province


host_tz = pytz.timezone('Africa/Harare')

def main():
    print('eTenders download in progress...')
    try:

        log_data = set()               # holds data from the log (i.e. urls, closing date, issue date, tender summary etc.)
        prog = re.compile('(\d\d/\d\d/\d\d\d\d)')
        with smart_open('https://s3.eu-west-2.amazonaws.com/leadshub-staticfiles/scraper_utils/etenders/e_portal_log.txt', encoding='utf-8', mode='r') as eportal_log_file:
            try:
                for line in eportal_log_file:
                    line_data_list = line.split(';', 6)
                    result = prog.match(line_data_list[3])
                    if result != None:
                        strippedDate = result.group(0)
                        closing_date = datetime.strptime(strippedDate, '%d/%m/%Y')
                        if closing_date > datetime.today():
                            log_data.add(line)
            except TypeError as e:
                print(e)

        # Below is the dictionary that contains Provinces to be chaecked for tenders on the etenders.gov.za platform.
        provinces_dict = {
            "Eastern Cape": 34,
            "Free State": 29,
            "Gauteng": 26,
            "KwaZulu Natal": 31,
            "Limpopo": 32,
            "Mpumalanga": 28,
            "North West": 27,
            "Northern Cape": 30,
            "Western Cape": 33,
            "National": 98
        }

        tender_location = Province.objects.none()   #To hold the location(s) of a tender.

        for province in provinces_dict:
            if province == "National":
                tender_location = Province.objects.exclude(province_name="Africa")
            else:
                tender_location = Province.objects.filter(province_name=province.strip())

            sauce = urllib.request.urlopen('https://etenders.treasury.gov.za/content/advertised-tenders')
            soup = BeautifulSoup(sauce, 'html.parser')


            last_tender_page = soup.find('li', {'class': 'pager-last last'}).a.get('href')

            tot_page_num = 0        #this is to hold the number of pages per Province searched for tenders.
            if last_tender_page != None:
                reg = re.compile('page=(\d+)$')
                tot_page_num = reg.search(last_tender_page).group(1)    #returns the number of pages that contain tenders.

            website_data = set()

            print(tot_page_num)

            t_counter = 0
            while t_counter <= int(tot_page_num):
                website_data.update(get_tender_page('https://etenders.treasury.gov.za/content/advertised-tenders?field_tender_category_tid=All&field_region_tid={}&field_sector_tid=All&field_testing_dept_tid=All&field_tender_type_tid=All&page={}'.format(provinces_dict[province], t_counter)))
                t_counter += 1

            website_data = website_data - log_data      #removes all the tenders that have already been sourced by checking the log.

            for entry in website_data:
                save_tender_to_db(entry, tender_location)

            log_data = log_data.union(website_data)



        bucketName = settings.AWS_STORAGE_BUCKET_NAME
        Key = "e_poral_log.txt"
        outPutname = "e_portal_log.txt"


        etenders_data = io.StringIO()
        etenders_data.writelines(log_data)

        s3 = boto3.resource(
            's3',
            region_name='eu-west-2',
            # endpoint_url='https://s3.eu-west-2.amazonaws.com/leadshub-staticfiles/scraper_utils/etenders',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        resp = s3.Object(
            settings.AWS_STORAGE_BUCKET_NAME,
            'scraper_utils/etenders/e_portal_log.txt'
        )
        resp.put(Body=etenders_data.getvalue())

        etenders_data.close()

    except urllib.error.URLError as e:
        print(e)

def get_tender_page(url):
    try:
        print(url)
        sauce_1 = urllib.request.urlopen(url)
        soup_1 = BeautifulSoup(sauce_1, 'html.parser')
        table_body = soup_1.find('div', {'class': 'view-content'}).tbody
        page_tenders = []
        if table_body != None:
            tr_tags = table_body.findAll('tr')
            for tr_tag in tr_tags:
                data_rec = []
                td_data = tr_tag.findAll('td')
                data_rec.append(td_data[1].a.get('href'))
                data_rec.append(td_data[2].text.strip())
                data_rec.append(td_data[3].text.strip())
                data_rec.append(td_data[4].text.strip())
                data_rec.append(td_data[5].text.strip())
                data_rec.append(td_data[1].a.text.strip())
                data_rec.append(td_data[0].text.strip())

                page_tenders.append(';'.join(data_rec).strip()+'\n')
        return page_tenders
    except urllib.error.URLError as e:
        print(e)
        return []


def save_tender_to_db(data_rec_str, t_location):
    try:
        url_data_ls = data_rec_str.strip().split(';', 6)
        sauce_2 = urllib.request.urlopen('https://etenders.treasury.gov.za{}'.format(url_data_ls[0]))
        soup_2 = BeautifulSoup(sauce_2, 'html.parser')

        # finds the container div in the html.
        container_tag = soup_2.findAll('div', {'class': 'fieldset-wrapper'})

        idSet = set()
        for x in range(3):
            idSet.add(random.randint(1, 61))

        try:
            tender_obj = Tender()
            tender_obj.buyersName = 'Place Holder'
            tender_obj.summary = str(url_data_ls[5]).strip()

            if len(url_data_ls[1].strip()) < 100:
                tender_obj.refNum = str(url_data_ls[1]).strip()

            tender_obj.issueDate = extract_date(url_data_ls[2].strip(), 1)
            tender_obj.closingDate = extract_date(url_data_ls[3].strip(), 2)

            if url_data_ls[4].strip() != '':
                tender_obj.siteInspectionDate = extract_date(url_data_ls[4].strip(), 2)

            tender_obj.description = str(container_tag[0])
            tender_obj.kw_assigned = True

            if len(container_tag) > 1:
                tender_obj.tDocLinks = str(container_tag[1])

            etenders_cat = Generic_cats.objects.none()

            tender_obj.save()

            try:
                etenders_cat = Generic_cats.objects.get(cat_description=url_data_ls[6].strip())
                tender_obj.assigned_keywords.set(etenders_cat.cat_kw.all())
            except Generic_cats.DoesNotExist as k:
                print(k)

            tender_obj.tenderCategory.set(Category.objects.filter(id__in=list(idSet)))
            tender_obj.tenderProvince.set(t_location)

            print(url_data_ls[1] + " - loaded")

        except TypeError as e:
            print(e)

    except urllib.error.URLError as e:
        print(e)


def extract_date(date_str, date_type):
    if date_type == 1:
        try:
            date = datetime.strptime(str(date_str), '%d/%m/%Y')
            tz_date = host_tz.localize(date)
            return tz_date
        except ValueError as e:
            print(e)
    else:
        try:
            date = datetime.strptime(str(date_str), '%d/%m/%Y - %I:%M%p')
            tz_date = host_tz.localize(date)
            return tz_date
        except ValueError as e:
            print(e)


if __name__ == '__main__': main()


