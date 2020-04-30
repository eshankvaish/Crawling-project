from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import model_scrape
from django.db import transaction

# Create your models here.

class SiteData(models.Model):
    site_name = models.CharField(max_length=255, null=False, default='')
    url = models.URLField(blank=False, unique=True, default='', null=False)
    regex = models.CharField(max_length=255, unique=True, null=False, default='')
    #regex for following fields
    name = models.CharField(max_length=255, default='')
    image = models.CharField(max_length=255, default='')
    startDate = models.CharField(max_length=255, default='')
    endDate = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=1000, default='')
    createdDate = models.DateField(auto_now=True)

    def __str__(self):
        return self.site_name

@receiver(post_save, sender = SiteData)
@transaction.atomic
def CrawlSite_call(sender, instance, **kwargs):
    non_interest = NonInterestingUrl.objects.create(sitedata = instance, url = instance.url)
    non_interest.save()
    site = {
        'base_url': non_interest.url,
        'regex': non_interest.sitedata.regex,
        'sitedata': non_interest.sitedata,
    }
    res = model_scrape.CrawlSite(site)
    non_interest.status = True
    non_interest.save()
    for i in res[0]:
        try:
            data = InterestingUrl(url = i, sitedata = instance)
            data.save()
        except:
            print("Exception in interest "+ i)
            break
    for i in res[1]:
        try:
            data = NonInterestingUrl(url = i, sitedata = instance)
            data.save() 
        except:
            print("Exception in non-interest" + i) 
            break
    print(str(len(res[0])) + " interesting urls added")
    print(str(len(res[1])) + " non-interesting urls added")  
    print(instance.site_name + " is Crawled Successfully")

class InterestingUrl(models.Model):
    sitedata = models.ForeignKey(SiteData, on_delete=models.CASCADE, related_name='interests')
    url = models.URLField(blank=False, unique=True, default='', null=False)
    name = models.CharField(max_length=255, default='')
    image = models.CharField(max_length=255, default='')
    startDate = models.CharField(max_length=255, default='')
    endDate = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=1000, default='')
    createdDate = models.DateField(auto_now=True)
    updatedDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)  #True if Crawled
    poor = models.BooleanField(default=False)

    class Meta:
        ordering = ['-createdDate']

class NonInterestingUrl(models.Model):
    sitedata = models.ForeignKey(SiteData, on_delete=models.CASCADE, related_name='non_interests')
    url = models.URLField(blank=False, unique=True, default='', null=False)
    createdDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    poor = models.BooleanField(default=False)

    class Meta:
        ordering = ['-createdDate']


