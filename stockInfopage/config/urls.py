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

#edit
from stockInfopage import views as search
urlpatterns = [
    path('admin/', admin.site.urls),
    path('company/', company.company),
    path('daily_price/', daily_price.daily_price),
    path('daily_price/<str:code>', detail.detail),#edit daily_price에서 티커명 클릭 시 세부 페이지로 이동
    path('',include('stockInfopage.urls')), # 페이징 시 URL이 해당 경로를 따라가도록 설정. stockInfopage의 urls.py 내용을 불러온다.
    path('dashboard/', dashboard.dashboard),
    path('dashboard/<str:code>', detail.detail),
    path('search/', search.search),

    #edit
    #path('lists/',lists.lists),
    #path('lists/<str:code>',detail.detail),
]