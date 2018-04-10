#!/opt/conda/bin/python
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import codecs
from rdautil import rdapublisher as pub
from rdautil import qualitychecks
import datetime
from datetime import date, timedelta
import logging


def get_driver():
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=inetproxy:3128')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("headless")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver   

def get_soup(driver,url):
    driver.get(url)
    body = driver.page_source
    soup = BeautifulSoup(body, 'lxml')
    text_file = codecs.open("Output.htm", "w", 'utf-8')
    text_file.write(body)
    text_file.close()
    return soup  
def replace(incident):
    if ',' in incident:
        return int(incident.replace(',',''))  
    else:
        return int(incident)  

def fix_frequency(one_per):
    try:
        split_string = one_per.split(" ")[1]
        if ',' in split_string:
            return int(split_string.replace(',',''))
        else:
            return int(split_string)
    except ValueError:   
        print(one_per)
    
    
  
def main():
    file = open("surnames.txt", "r")
    name = file.readlines()    
    rows=[] 
    for surname in name:  
        driver = get_driver()
        url = 'http://forebears.io/surnames'
        url = url + '/' + surname
        print(url)
        soup = get_soup(driver, url)
        table = soup.find('table',attrs={ "id" : "nations2014"})
        driver.get_screenshot_as_file('temp.png')
        for row in table.find_all('tr'):
            data = row.find_all("td")
            if len(data) > 0:
                tmp = []
                tmp = [td.text for td in row.find_all('td')]
                tmp.append(surname.rstrip())
                rows.append(tmp)
                  
            else:
                print('Header row') 
    df = pd.DataFrame(rows,columns = ['country', 'incidence', 'one_per', 'rank_in_nation', 'surname'])
    print(df)
    df['incidence'] = df['incidence'].apply(replace)
    df['one_per'] =df['one_per'].apply(fix_frequency)
    df = df.set_index(['country'])
    yesterday = date.today() - timedelta(1)
    runDate = yesterday.strftime('%Y%m%d')
    result = qualitychecks.run_all_checks(df, 'forebears', 'surname',runDate)
    pub.publish_dataset(df, result, 'forebears', 'surname')  
    
if __name__ == '__main__' :
    main()       #!/opt/conda/bin/python
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import codecs
from rdautil import rdapublisher as pub
from rdautil import qualitychecks
import datetime
from datetime import date, timedelta
import logging


def get_driver():
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=inetproxy:3128')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("headless")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver   

def get_soup(driver,url):
    driver.get(url)
    body = driver.page_source
    soup = BeautifulSoup(body, 'lxml')
    text_file = codecs.open("Output.htm", "w", 'utf-8')
    text_file.write(body)
    text_file.close()
    return soup  
def replace(incident):
    if ',' in incident:
        return int(incident.replace(',',''))  
    else:
        return int(incident)  

def fix_frequency(one_per):
    try:
        split_string = one_per.split(" ")[1]
        if ',' in split_string:
            return int(split_string.replace(',',''))
        else:
            return int(split_string)
    except ValueError:   
        print(one_per)
    
    
  
def main():
    file = open("surnames.txt", "r")
    name = file.readlines()    
    rows=[] 
    for surname in name:  
        driver = get_driver()
        url = 'http://forebears.io/surnames'
        url = url + '/' + surname
        print(url)
        soup = get_soup(driver, url)
        table = soup.find('table',attrs={ "id" : "nations2014"})
        driver.get_screenshot_as_file('temp.png')
        for row in table.find_all('tr'):
            data = row.find_all("td")
            if len(data) > 0:
                tmp = []
                tmp = [td.text for td in row.find_all('td')]
                tmp.append(surname.rstrip())
                rows.append(tmp)
                  
            else:
                print('Header row') 
    df = pd.DataFrame(rows,columns = ['country', 'incidence', 'one_per', 'rank_in_nation', 'surname'])
    print(df)
    df['incidence'] = df['incidence'].apply(replace)
    df['one_per'] =df['one_per'].apply(fix_frequency)
    df = df.set_index(['country'])
    yesterday = date.today() - timedelta(1)
    runDate = yesterday.strftime('%Y%m%d')

    
if __name__ == '__main__' :
    main()       
