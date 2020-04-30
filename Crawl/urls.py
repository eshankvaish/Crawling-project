from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('admin/scrawler/', views.scrawler, name = 'scrawler'),
    path('admin/scrawler/scrape', views.scrape, name = 'scrape'),
]