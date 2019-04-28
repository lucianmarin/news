""" https://docs.djangoproject.com/en/2.1/topics/http/urls/ """

from django.urls import path
from app import api, views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/top/', api.top, name='api_top'),
    path('api/recent/', api.recent, name='api_recent'),
    path('api/read/<int:id>/', api.read, name='api_read'),
    path('commented/', views.commented, name='commented'),
    path('reacted/', views.reacted, name='reacted'),
    path('recent/', views.recent, name='recent'),
    path('about/', views.about, name='about'),
    path('light/', views.light, name='light'),
    path('dark/', views.dark, name='dark'),
    path('<str:domain>/', views.site_index, name='site_index'),
    path('<str:domain>/recent/', views.site_recent, name='site_recent'),
    path('read/<int:id>/', views.read, name='read')
]
