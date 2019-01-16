""" https://docs.djangoproject.com/en/2.1/topics/http/urls/ """

from django.urls import path
from app import api, views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/top/', api.top, name='api_top'),
    path('api/recent/', api.recent, name='api_recent'),
    path('api/text/<int:id>/', api.text, name='api_text'),
    path('recent/', views.recent, name='recent'),
    path('about/', views.about, name='about'),
    path('<str:domain>/', views.site_index, name='site_index'),
    path('<str:domain>/recent/', views.site_recent, name='site_recent'),
    path('text/<int:id>/', views.text, name='text')
]
