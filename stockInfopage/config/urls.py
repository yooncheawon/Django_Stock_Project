from django.contrib import admin
from django.urls import path, include
from stockInfopage import views as detail
from django.urls import path
from stockInfopage.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

]



