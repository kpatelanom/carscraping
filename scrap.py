from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

url = "https://droom.in/cars"
driver = webdriver.Chrome(
    'Driver path')
driver.get(url)
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
all_divs = soup.find_all(
    'div', {'class': 'jss210 card-body'})

links = []
for div in all_divs:
    aa = div.find('a', href=True)
    links.append(aa['href'])

driver.close()
count = 1
for link in links:
    count += 1
    driver = webdriver.Chrome(
        'driver path')
    driver.get(link)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', {
                    'class': 'd-position-relative d-padding-20 d-padding-top-15 d-padding-bottom-0 listing-card'})
    print(div.text)
    driver.close()
    if count == 2:
        break
header = ['name', 'used', 'km', 'fuel', 'owner', 'location', 'selling price']

with open('spinnyData.csv', 'w', encoding='UTF8') as f:
     writer = csv.writer(f)

     writer.writerow(header)
     for div in all_divs:
         data = []
         model = div.find(
             'div', {'class': 'styles__yearAndMakeAndModelSection'}).text
         km = div.find('p', {'class': 'styles__otherInfoSection'}).text
         price = div.find('div', {'class': 'styles__priceSection'}).text
         data.append(model)
         if km[8] == 'p':
             if km[len(km) - 1] == 'c':
                 data.append(km.replace('petrolautomatic', ''))
             else:
                 data.append(km.replace('petrolmanual', ''))
             data.append('petrol')
         else:
             if km[len(km) - 1] == 'c':
                 data.append(km.replace('dieselautomatic', ''))
             else:
                 data.append(km.replace('dieselmanual', ''))
             data.append('diesel')
        if km[len(km) - 1] == 'c':
            data.append('automatic')
         else:
             data.append('manual')
         data.append(price.replace('‚¹', ''))
         writer.writerow(data)


driver.close()
