from django.db import models
from django.contrib.auth.models import AbstractUser

from mutualfunds.models import MutualFunds



# class User(AbstractUser):
#     email=models.EmailField(unique=True)
#     USERNAME_FIELD='email'
#     username = None
#     REQUIRED_FIELDS=[]
#     objects=CustomUserModel()


#     class Meta:
#         verbose_name='User'
#         verbose_name_plural="Users"


#     def __str__(self):
#         return self.email




class User(AbstractUser):
    email = None



class UserInvestment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="users_investment")
    mutual_fund = models.ForeignKey(MutualFunds,on_delete=models.CASCADE,related_name="users_mutual_fund")
    units = models.FloatField()


    