from django.contrib import admin
from .models import SiteData, InterestingUrl, NonInterestingUrl
# Register your models here.

@admin.register(SiteData)
class SiteDataAdmin(admin.ModelAdmin):
    list_display = ('id','site_name','url','createdDate',)
    search_fields = ['site_name']
    list_filter = ('createdDate',)

@admin.register(InterestingUrl)
class InterestingUrlAdmin(admin.ModelAdmin):
    list_display = ('id','sitedata','url','status','createdDate',)
    search_fields = ['sitedata']
    list_filter = ('createdDate','status')  

@admin.register(NonInterestingUrl)
class NonInterestingUrlAdmin(admin.ModelAdmin):
    list_display = ('id','sitedata','url','createdDate',)
    search_fields = ['sitedata']
    list_filter = ('createdDate',)  


