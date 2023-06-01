from django.urls import path

from . import views

app_name = 'stockInfopage'

urlpatterns = [
    path('home/', views.home, name='home'),
]