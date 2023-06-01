"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from stockInfopage import views as daily_price
from stockInfopage import views as company
# from stockInfopage import views as home
from stockInfopage import views as dashboard
# from stockInfopage import views as lists
from stockInfopage import views as detail

from django.urls import path
from stockInfopage.views import home

#edit
from stockInfopage import views as search
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('stockInfopage.urls')), # 페이징 시 URL이 해당 경로를 따라가도록 설정. stockInfopage의 urls.py 내용을 불러온다.
    path('dashboard/<str:code>', detail.detail),
    path('', home, name='home'),

]



