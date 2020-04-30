from django.db import models

# Create your models here.

class SiteData(models.Model):
    site_name = models.CharField(max_length=255, null=False, default='')
    url = models.URLField(blank=False, unique=True, default='', null=False)
    site_regex = models.CharField(max_length=255, unique=True, null=False, default='')
    regex = models.CharField(max_length=255, unique=True, null=False, default='')
    add_base_url = models.BooleanField(default=False)
    #regex for following fields
    name = models.CharField(max_length=255, default='')
    image = models.CharField(max_length=255, default='')
    startDate = models.CharField(max_length=255, default='')
    endDate = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=1000, default='')
    createdDate = models.DateField(auto_now=True)

    def __str__(self):
        return self.site_name

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

    class Meta:
        ordering = ['-createdDate']

class NonInterestingUrl(models.Model):
    sitedata = models.ForeignKey(SiteData, on_delete=models.CASCADE, related_name='non_interests')
    url = models.URLField(blank=False, unique=True, default='', null=False)
    createdDate = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-createdDate']


