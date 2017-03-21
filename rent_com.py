import urllib2
from bs4 import BeautifulSoup
import math
import csv

def rentcomData():
    baseUrl = 'http://www.rent.com/%s/%s/apartments_condos_houses_townhouses%s'

    cityState = [('new-york', 'new-york'), ('illinois', 'chicago'), ('south-carolina', 'charleston'),
                 ('nevada', 'las-vegas'),
                 ('washington', 'seattle'), ('california', 'san-francisco'), ('district-of-columbia', 'washington'),
                 ('louisiana', 'new-orleans'), ('california', 'palm-springs'), ('california', 'san-diego'),
                 ('missouri', 'saint-louis'),
                 ('arizona', 'sedona'), ('hawaii', 'honolulu'), ('florida', 'miami-beach'), ('missouri', 'branson'),
                 ('massachusetts', 'boston'), ('georgia', 'savannah'), ('florida', 'orlando'), ('oregon', 'portland'),
                 ('hawaii', 'lahaina'), ('florida', 'saint-augustine'), ('tennessee', 'nashville'),
                 ('california', 'los-angeles'),
                 ('texas', 'san-antonio'), ('texas', 'austin')]
    bedroom = ['_1-bedroom', '_2-bedroom', '_3-bedroom']

    citys = ['City']
    prices = ['Price']
    addressList = ['Address']
    rentbuy = ['Type']
    zipcode = ['Zipcode']
    numBed = ['Number of Bedrooms']
    numBath = ['Number of Bathrooms']
    for city in cityState:
        for bed in bedroom:
            URL = baseUrl % (city[0], city[1], bed)
            request = urllib2.Request(URL, headers={'User-Agent': "Resistance is futile"})
            response = urllib2.urlopen(request)
            html = BeautifulSoup(response, 'html.parser')
            totalCount = int(html.find('span', {'class': 'total-listings-count'}).get_text())
            if totalCount >= 20:
                pageTotal = math.ceil(int(html.find('span', {'class': 'total-listings-count'}).get_text()) / 20)
            else:
                pageTotal = 1
            for i in range(int(pageTotal)):
                newURL = URL + '?page=' + str(i + 1)
                newReq = urllib2.Request(newURL, headers={'User-Agent': "Resistance is futile"})
                response = urllib2.urlopen(newReq)
                html = BeautifulSoup(response, 'html.parser')
                items = html.find_all('div', {'class': 'prop li-srp'})
                for item in items:
                    price = str(item.find('p', {'class': 'prop-rent bullet-separator strong'}).get_text())
                    if price != 'Contact for Pricing':
                        if 'From' in price:
                            prices.append(int(price[6:]))
                        elif ' ' not in price:
                            prices.append(int(price[1:]))
                        else:
                            prices.append(int(price[1:price.index(' ')]))
                        citys.append(city[1])
                        rentbuy.append('rent')
                        link = item.a['href']
                        res = urllib2.urlopen('http://www.rent.com' + link)
                        ht = BeautifulSoup(res, 'html.parser')
                        address = str(ht.find('span', {'itemprop': 'streetAddress'}).get_text())
                        addressList.append(address)
                        postal = str(ht.find('span', {'itemprop': 'postalCode'}).get_text())
                        zipcode.append(postal)
                        numOfBed = str(item.find('span', {'class': 'prop-beds bullet-separator'}).get_text())
                        numBed.append(int(numOfBed[0]))
                        numOfBath = str(item.find('span', {'class': 'prop-baths bullet-separator'}).get_text())
                        numBath.append(int(numOfBath[0]))
    output = zip(addressList, zipcode, prices, rentbuy, citys, numBed, numBath)
    with open('rent_com.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in output:
            writer.writerow(row)

