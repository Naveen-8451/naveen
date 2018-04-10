#!/opt/conda/bin/python
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import codecs
import time
from datetime import date as dt
from datetime import timedelta
from rdautil import pubhelper as p

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=proxy:3128')
    #chrome_options.add_argument('--proxy-server=proxy.wellmanage.com:8080')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("headless")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def get_soup(driver, url):
    driver.get(url)
    time.sleep(3)
    body = driver.page_source

    text_file = codecs.open("/tmp/Output.htm", "w", 'utf-8')
    text_file.write(body)
    text_file.close()


    soup = BeautifulSoup(body, 'lxml')
    return soup


def get_zips(soup) :
    towns = soup.find_all("span", class_="locality")
    zips = []
    for town in towns:
        zip = town.get_text().split(" ")[-1]
        zip = zip.rjust(5, '0')
        zips.append(zip)

    return zips

def get_other_countries(countries, soup, region) :
    apac = soup.find("div", class_=region)
    apacs = apac.find_all("a")

    for lnk in apacs:
        code = lnk["rel"][0]
        #dont add us because we do by zip code
        if code != 'en_US' :
            countries.append({'region' : region,  'code': code})

    return countries

def get_cars(cars, driver, region, code, zip) :
    url = 'https://www.tesla.com/'
    if code :
        url = url + code + '/'
    url = url + 'new?redirect=no'
    if zip :
        url = url + '&zip=' + zip

    soup = get_soup(driver, url)

    print("DONE ", url)
    letters = soup.find_all("div", class_='vehicle')
    for letter in letters:
        href = letter.find("a", class_="vehicle-link")
        model = letter.find("div", class_="model-name")
        battery = letter.find("div", class_="battery-badge")

        if not href is None:
            battery_type = battery.find("h1").getText()
            vin = href["href"].split('/')[-1]
            cars.append({'model': model.getText(),
                         'region' : region,
                         'code': code,
                         'zip': zip,
                         'vin': vin,
                         'seq': vin[-6:],
                         'battery': battery_type})

    print("DONE ", url, len(cars))

    return cars

def main() :
    driver = get_driver()
    soup = get_soup(driver, 'https://www.tesla.com/findus/list/stores/United+States')

    zips = get_zips(soup)

    countries = []
    get_other_countries(countries, soup, "region-apac")
    get_other_countries(countries, soup, "region-northamerica")
    get_other_countries(countries, soup, "region-europe")
    get_other_countries(countries, soup, "region-middle-east")

    print(countries)

    cars = []
    for zip in zips:
        get_cars(cars, driver, 'region-northamerica', None, zip)
    for country in countries:
        get_cars(cars, driver, country['region'], country['code'], None)

    print(cars)

    df = pd.DataFrame(cars, columns=['vin', 'index', 'battery', 'code', 'model', 'region', 'seq', 'zip'])

    yesterday = dt.today() - timedelta(1)
    run_date = yesterday.strftime('%Y%m%d')
    df['run_date'] = run_date

    pub = p.PubHelper('tesla', 'inventory', run_date, True)
    pub.publish(df, 'Y')

    pass


if __name__ == '__main__' :
    main()
