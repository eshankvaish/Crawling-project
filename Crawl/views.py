from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SiteData, InterestingUrl, NonInterestingUrl
from . import Scrape
# Create your views here.

@login_required
def home(request):
    return render(request, 'base.html')

@login_required
def scrawler(request):
    non_interest = None
    try:
        non_interest = NonInterestingUrl.objects.all().latest('id')
        site = {
            'base_url': non_interest.url,
            'regex': non_interest.sitedata.regex,
            'add_base_url': non_interest.sitedata.add_base_url,
            'site_regex': non_interest.sitedata.site_regex,
            'sitedata': non_interest.sitedata,
        }
        Scrape.CrawlSite(site)
        return render(request, 'base.html', {'res': f'Data was crawled successfully for {site["base_url"]}'})
    except:
        return render(request, 'base.html', {'res': 'There was some error...'})

@login_required
def scrape(request):
    try:
        interest = InterestingUrl.objects.all().filter(status = False).latest('id')
        site = {
            'pk': interest.pk,
            'url': interest.url,
            'name': interest.sitedata.name,
            'image': interest.sitedata.image,
            'startDate': interest.sitedata.startDate,
            'endDate': interest.sitedata.endDate,
            'description': interest.sitedata.description,
        }
        response = Scrape.scrape(site)
        if response:
            return render(request, 'base.html', {'res': f'Id = {site["pk"]} Data was scraped successfully'})
        else:
            return render(request, 'base.html', {'res': 'There was some updation error...'}) 
    except:
        return render(request, 'base.html', {'res': 'There was some error...'})



