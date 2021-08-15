from django.db import models

# Create your models here.
class HarborData(models.Model):
    date = models.CharField(max_length=30)
    shipname = models.CharField(max_length=30)
    worktype = models.CharField(max_length=20)