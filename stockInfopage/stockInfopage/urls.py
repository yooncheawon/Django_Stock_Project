from django.urls import path

from . import views

app_name = 'stockInfopage'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('company/', views.company, name='company'),
    path('daily_price/', views.daily_price, name='daily_price'),
    path('detail/', views.daily_price, name='detail'),#edit
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
]