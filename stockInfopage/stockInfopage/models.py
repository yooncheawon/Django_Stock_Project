from django.db import models

from jsonfield import JSONField


class Company(models.Model):
    code = models.CharField(max_length=20, primary_key= True)
    company = models.CharField(max_length=40)
    last_update = models.DateField()

    def __str__(self):
        return self.company
