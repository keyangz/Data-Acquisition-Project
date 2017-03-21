import urllib2
from bs4 import BeautifulSoup
import math

def getSalesData():
    cityState = [('New_York', 'NY'), ('Chicago', 'IL'), ('Charleston', 'SC'), ('Las_Vegas', 'NV'),
                 ('Seattle', 'WA'), ('San_Francisco', 'CA'), ('Washington', 'DC'),
                 ('New_Orleans', 'LA'), ('Palm_Springs', 'CA'), ('San_Diego', 'CA'), ('Saint_Louis', 'MO'),
                 ('Sedona', 'AZ'), ('Honolulu', 'HI'), ('Miami_Beach', 'FL'), ('Branson', 'MO'),
                 ('Boston', 'MA'), ('Savannah', 'GA'), ('Orlando', 'FL'), ('Portland', 'OR'),
                 ('Lahaina', 'HI'), ('Saint_Augustine', 'FL'), ('Nashville', 'TN'), ('Los_Angeles', 'CA'),
                 ('San_Antonio', 'TX'), ('Austin', 'TX')]
    citys = []
    prices = []
    addressList = []
    rentbuy = []
    zipcodes = []
    numBed = []
    numBath = []
    for city in cityState:
        baseURL = 'https://www.trulia.com/for_sale/' + city[0] + ',' + city[1] + '/1p_beds/1p_baths/'
        request = urllib2.Request(baseURL, headers={'User-Agent': "Resistance is futile"})
        response = urllib2.urlopen(request)
        html = BeautifulSoup(response, 'html.parser')
        totalResultStr = str(html.find('div', {'class': 'txtC h6 typeWeightNormal typeLowlight'}).get_text())[10:]
        totalCount = int(totalResultStr[0:totalResultStr.index(' ')])
        if totalCount >= 30:
            pageTotal = math.ceil(totalCount / 30)
        else:
            pageTotal = 1
        for i in range(int(pageTotal)):
            pageURL = baseURL + str(i + 1) + '_p/'
            pageReq = urllib2.Request(pageURL, headers={'User-Agent': "Resistance is futile"})
            pageRep = urllib2.urlopen(pageReq)
            pagehtml = BeautifulSoup(pageRep, 'html.parser')
            items = pagehtml.find_all('div', {'class': 'smlCol12 lrgCol8 ptm cardContainer'})
            for item in items:
                citys.append(city[0].replace('_', ' '))
                rentbuy.append('buy')
                link = item.a['href']
                zipcode = link[-5:]
                zipcodes.append(zipcode)
                newURL = 'https://www.trulia.com' + link
                newReq = urllib2.Request(newURL, headers={'User-Agent': "Resistance is futile"})
                newRep = urllib2.urlopen(newReq)
                newhtml = BeautifulSoup(newRep, 'html.parser')
                price = str(
                    newhtml.find('div', {'class': 'h2 typeReversed typeDeemphasize man pan noWrap'}).get_text()).strip()
                prices.append(int(price.replace(',', '')[1:]))
                address = str(
                    newhtml.find('span',
                                 {'class': 'headingDoubleSuper h2 typeWeightNormal mvn ptn'}).get_text()).strip()
                addressList.append(address)
                bedBath = item.find(class_="cardDetails man ptm phm")
                numOfBed = bedBath.find(class_="iconBed").parent.text
                numBed.append(int(numOfBed[0]))
                numOfBath = bedBath.find(class_='iconBath').parent.text
                numBath.append(int(numOfBath[0]))
    output = zip(citys, prices, addressList, rentbuy, zipcodes, numBed, numBath)
    return output



