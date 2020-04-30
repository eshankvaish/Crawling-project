import requests, re
from bs4 import BeautifulSoup
from .models import InterestingUrl, NonInterestingUrl
import datetime

"""
site = {
    'base_url':'',
    'regex':'',
    'add_base_url': True/False,
                    #regex for event attributes
    'site_regex': '',
    'name': '',
    'image': '',
    'startDate':'',
    'endDate':'',
    'description':'',
}

"""

def CrawlSite(site):
    req = requests.get(site['base_url']).text
    soup = BeautifulSoup(req, "html.parser")
    a = soup.find_all('a', {'href': re.compile(rf'{site["site_regex"]}')})
    anew = soup.find_all('a', {'href': re.compile(rf'{site["regex"]}')})
    non_interest = set()
    interest = set()

    if site['add_base_url']:
        add_url = site['base_url']
    else:
        add_url = ''

    for i in a:
        non_interest.add(i['href'])
    for i in anew:
        interest.add(add_url + i['href'])
    non_interest -= interest
    addInterest(interest, site['sitedata'])
    addNonInterest(non_interest, site['sitedata'])
    print("Crawled Data from " + site['base_url'] + "successfully")
    

def addInterest(interest, sitedata):
    for i in interest:
        try:
            data = InterestingUrl(url = i, sitedata = sitedata)
            data.save()
        except:
            pass 

def addNonInterest(non_interest, sitedata):
    for i in non_interest:
        try:
            data = NonInterestingUrl(url = i, sitedata = sitedata)
            data.save() 
        except:
            pass

def scrape(site):
    req = requests.get(site['url']).text
    soup = BeautifulSoup(req, "html.parser")
    data = str(soup.find_all('script', type = "application/ld+json"))
    info = {
        'name': (re.compile(rf'{site["name"]}')).search(data).group(0)[8:-2].split('"')[0],
        'image': (re.compile(rf'{site["image"]}')).search(data).group(0)[9:-2],
        'startDate': (re.compile(rf'{site["startDate"]}')).search(data).group(0)[13:23],
        'endDate': (re.compile(rf'{site["endDate"]}')).search(data).group(0)[11:21],
        'description': (re.compile(rf'{site["description"]}')).search(data).group(0)[17:-2],
    }
    print("Scrapped Data is:")
    for j in info:
        print(j + ":" + info[j])
    #TODO : dates
    try:
        interest = InterestingUrl.objects.get(pk= site['pk'])
        interest.name = info['name']
        interest.image = info['image']
        interest.status = True
        interest.startDate = info['startDate']
        interest.endDate = info['endDate']
        interest.description = info['description'][:1000]
        interest.save()
        return True
    except:
        return False
    
        
        