import requests, re
from bs4 import BeautifulSoup
from .models import InterestingUrl, NonInterestingUrl
import datetime

"""
site = {
    'base_url':'',
    'regex':'',
        #regex for event attributes
    'name': '',
    'image': '',
    'startDate':'',
    'endDate':'',
    'description':'',
}

"""

def CrawlSite(site):
    req = requests.get(site['base_url'])
    if req.status_code != 200:
        non_interest = NonInterestingUrl.objects.get(pk= site['pk'])
        non_interest.poor = True
        non_interest.save()
        print("POOR Url...")
        return
    soup = BeautifulSoup(req.text, "html.parser")
    a = soup.find_all('a', href = True)
    anew = soup.find_all('a', {'href': re.compile(rf'{site["regex"]}')})
    non_interest = set()
    interest = set()
    n=0
    for i in a:
        if n>=10:
            break
        if i['href'][0]=='/':
            non_interest.add(site['base_url'] + i['href'])
            n+=1
        elif i['href'][:len(site['base_url'])]==site['base_url']:
            non_interest.add(i['href'])
            n+=1
    n=0
    for i in anew:
        if n>=10:
            break
        if i['href'][0]=='/':
            interest.add(site['base_url'] + i['href'])
            n+=1
        else:
            interest.add(i['href'])
            n+=1
    non_interest -= interest
    print(site['base_url'])
    print("Crawled Data from " + site['base_url'] + "successfully")
    print(interest)
    if interest=={}:
        non_interest = NonInterestingUrl.objects.get(pk= site['pk'])
        non_interest.poor = True
        non_interest.save()
        print("POOR Url...")
        return
    addInterest(interest, site['sitedata'])
    addNonInterest(non_interest, site['sitedata'])    

def addInterest(interest, sitedata):
    for i in interest:
        try:
            data = InterestingUrl(url = i, sitedata = sitedata)
            data.save()
        except:
            pass
    print(str(len(interest)) + " interesting urls added") 

def addNonInterest(non_interest, sitedata):
    for i in non_interest:
        try:
            data = NonInterestingUrl(url = i, sitedata = sitedata)
            data.save() 
        except:
            pass
    print(str(len(non_interest)) + " non-interesting urls added")

def scrape(site):
    print('Scraping for ' + site['url'])
    req = requests.get(site['url'])
    if req.status_code != 200:
        interest = InterestingUrl.objects.get(pk= site['pk'])
        interest.poor = True
        interest.save()
        print("POOR Url...")
        return False
    soup = BeautifulSoup(req.text, "html.parser")
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
    try:
        interest = InterestingUrl.objects.get(pk= site['pk'])
        interest.name = info['name']
        interest.image = info['image']
        interest.status = True
        interest.startDate = info['startDate']
        interest.endDate = info['endDate']
        interest.description = info['description'][:1000]
        interest.save()
        print("Scraped Data for " + site['url'] + "Successfully")
        return True
    except:
        return False
    
        
        