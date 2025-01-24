from django.db import models

from mutualfunds.enums import MutualFundsChoice

# Create your models here.

class MutualFunds(models.Model):
    name = models.CharField(max_length=255)
    fund_type = models.CharField(max_length=255,choices=MutualFundsChoice.choices)
    nav = models.FloatField()

