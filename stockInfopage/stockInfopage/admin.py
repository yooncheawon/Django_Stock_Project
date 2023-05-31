from django.contrib import admin
# 어플리케이션마다 admin이 있다.
from .models import Company



admin.site.register(Company)
