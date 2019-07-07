# import csv
#
# tempHolder = []
# with open('keywords.csv') as f:
#     reader = csv.reader(f, delimiter=';')
#     count = 0
#     for row in reader:
#         tempHolder.append(row[0].strip())
#
#         if(count == 44223):
#             break
#         count += 1
#
#
# with open('cleanedKeywords.txt', 'w') as f2:
#     for entry in tempHolder:
#         if len(entry.strip()) < 150:
#             f2.write(entry.strip()+'\n')


import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('LeadsHub-473e833e9627.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('categories').sheet1
    print(wks.get_all_records())


from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')
sched.start()