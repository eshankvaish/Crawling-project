from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SiteData, InterestingUrl, NonInterestingUrl
from . import Scrape
# Create your views here.

@login_required
def home(request):
    try:
        non_interest = NonInterestingUrl.objects.all()
        crawled = non_interest.filter(status = True, poor = False)
        interest = InterestingUrl.objects.all()
        scraped = interest.filter(status = True, poor = False).order_by('-id')
        return render(request, 'base.html', {
            'data': True,
            'non_interest': non_interest,
            'interest': interest,
            'crawled': crawled,
            'scraped': scraped,
        })
    except:
        return render(request, 'base.html')

@login_required
def scrawler(request):
    non_interest = None
    try:
        non_interest = NonInterestingUrl.objects.all().filter(status = False, poor = False).latest('id')
        site = {
            'pk': non_interest.pk,
            'base_url': non_interest.url,
            'regex': non_interest.sitedata.regex,
            'sitedata': non_interest.sitedata,
        }
        Scrape.CrawlSite(site)
        non_interest.status = True
        non_interest.save()
        return render(request, 'base.html', {'res': f'Data was crawled successfully for {site["base_url"]}'})
    except:
        return render(request, 'base.html', {'res': 'There was some error...'})

@login_required
def scrape(request):
    try:
        interest = InterestingUrl.objects.all().filter(status = False, poor = False).latest('id')
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
            return render(request, 'base.html', {'res': 'There was some error with the url...'}) 
    except:
        return render(request, 'base.html', {'res': 'There was some error...'})



