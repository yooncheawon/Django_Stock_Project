from django.db import models

from jsonfield import JSONField


# Create your models here.

class Company(models.Model):
    code = models.CharField(max_length=20, primary_key= True)
    company = models.CharField(max_length=40)
    last_update = models.DateField()

    def __str__(self):
        return self.company

class Daily(models.Model):
    code = models.CharField(max_length=128,primary_key=True)
    company = models.CharField(max_length=40)
    date = models.DateField()
    open = models.BigIntegerField()
    high = models.BigIntegerField()
    low = models.BigIntegerField()
    close = models.BigIntegerField()
    diff = models.BigIntegerField()
    volume = models.BigIntegerField()
    
    def __str__(self):
        return self.code

class Detaildaily(models.Model):
    code = models.CharField(max_length=128)
    company = models.CharField(max_length=40)
    date = models.DateField(primary_key=True)
    open = models.BigIntegerField()
    high = models.BigIntegerField()
    low = models.BigIntegerField()
    close = models.BigIntegerField()
    diff = models.BigIntegerField()
    volume = models.BigIntegerField()

    def __str__(self):
        return self.code