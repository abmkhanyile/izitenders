from bs4 import BeautifulSoup
import urllib.request

def main():
    sauce = urllib.request.urlopen("http://www.durban.gov.za/Resource_Centre/Tenders/Pages/default.aspx?Filter=1&View={FDF9F978-158E-41E8-A62B-23E75EDA6E6B}")
    soup = BeautifulSoup(sauce, 'html.parser')
    dates = soup.find('select', id="diidFilterClosing_x0020_Date").find_all('option')

    for dateTag in dates:
        print(dateTag.text)


if __name__ == '__main__': main()