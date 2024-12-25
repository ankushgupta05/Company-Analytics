from django.contrib import admin
from django.urls import path,include
from analytics import  views
urlpatterns = [
    path('',views.analytics,name='company-name-analytics'),
]
