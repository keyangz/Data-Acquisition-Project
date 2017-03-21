import urllib2
from bs4 import BeautifulSoup
import time
import random


def fetch(url,delay=(2,5)):
    """Simulate human random clicking 2..5 seconds then fetch URL.
    Returns the actual page source fetched and the HTML object."""

    time.sleep(random.randint(delay[0], delay[1]))
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    except ValueError as e:
        print str(e)
        return '', BeautifulSoup('', "html.parser")
    except:
        return '', BeautifulSoup('', "html.parser")

    pagedata = response.read()
    html = BeautifulSoup(pagedata, "html.parser")
    return (pagedata,html)


def parse_craigslist():
    soup = fetch("https://sfbay.craigslist.org/search/rea?s=0&bathrooms=1&bedrooms=1")
    i = 1
    for row in soup[1].find_all(class_="row"):
        pricetag = row.find_all(class_="price")
        if len(pricetag) > 0:
            print pricetag[0].text, i
            i += 1


parse_craigslist()

