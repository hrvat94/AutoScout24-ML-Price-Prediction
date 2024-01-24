import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

def getURLfromAS24(make, model, fuel, gear, year, kmfrom, kmto, powerfrom, powerto, offer):
    url = f"""
        https://www.autoscout24.de
        /lst
        /{make}
        /{model}
        ?atype=C
        &fuel={fuel}
        &gear={gear}
        &fregfrom={year}
        &fregto={year}
        &kmfrom={kmfrom}
        &kmto={kmto}
        &powerfrom={powerfrom}
        &powerto={powerto}
        &powertype=kw
        &offer={offer}
        &cy=D
        &damaged_listing=exclude
        &desc=1
        &ocs_listing=include
        &search_id=26qbsnxndak
        &size=20
        &sort=standard
        &ustate=N%2CU""".replace('\n','').replace(' ','')
    return url


def get_carsData(url):
    price_list = []
    car_title = []
    car_text = []
    car_link = []
    car_image = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    for el in soup.find_all("p", {'class': 'Price_price__APlgs PriceAndSeals_current_price__ykUpx'}):
        price_list.append(int(el.get_text()[2:-2].replace('.','')))
    for el in soup.find_all("a", {'class': 'ListItem_title__ndA4s ListItem_title_new_design__QIU2b Link_link__Ajn7I'}):
        car_title.append(el.h2.text)
        car_text.append(el.h2.span.text)
        car_link.append('https://www.autoscout24.de' + el['href'])
    for el in soup.find_all("source"):
        car_image.append(el['srcset'])

    km = []
    getriebe = []
    erstzulassung = []
    kraftstoff = []
    leistung = []
    verbrauch = []
    i = 0
    for el in soup.find_all("span", {'class': 'VehicleDetailTable_item__4n35N'}):
        print(el.text)
        if i == 0:
            km.append(el.text)
        elif i == 1:
            getriebe.append(el.text)
        elif i == 2:
            erstzulassung.append(el.text)
        elif i == 3:
            kraftstoff.append(el.text)
        elif i == 4:
            verbrauch.append(el.text)
        elif i == 5:
            leistung.append(el.text)
        if i == 5:
            i = 0
        else:
            i += 1
    
    return [price_list, car_title, car_text, car_link, car_image, km, getriebe, erstzulassung, kraftstoff, verbrauch, leistung]