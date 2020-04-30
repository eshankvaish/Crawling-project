#this is for post_save function to counter Circular Import Error

import requests, re
from bs4 import BeautifulSoup
import datetime

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
    print("Crawled Data from " + site['base_url'] + "successfully")
    if interest is None:
        non_interest = NonInterestingUrl.objects.get(pk= site['pk'])
        non_interest.poor = True
        non_interest.save()
        print("POOR Url...")
        return
    return [interest, non_interest]