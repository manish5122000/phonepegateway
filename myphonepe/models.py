from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=20,default='')
    Second_Name = models.CharField(max_length=20,default='')
    bio =models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    Phone_Number = models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=200,blank=True)




    def __str__(self):
        return f"{self.user.username}-{self.code}"

class PaymentDetail(models.Model):
    name = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=150)
    image = models.ImageField(upload_to='payment')
    datetime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} - {self.transaction_id} ({self.datetime.strftime('%Y-%m-%d %H:%M:%S')})"
    
class PaymentInitiate(models.Model):
    amount = models.IntegerField()
    source = models.CharField(max_length=150, blank=True)
    transaction_id = models.CharField(max_length=150)
    status = models.CharField(max_length=500)
    def __str__(self):
        return self.name
    
class Security(models.Model):
    ACCOUNT_SID = models.CharField(blank=True,max_length=200)
    AUTH_TOKEN = models.CharField(blank=True,max_length=200)
    VARIFY_SID = models.CharField(blank=True,max_length=200)



class PaymentSecret(models.Model):
    merchantid = models.CharField(max_length=200)
    key = models.CharField(max_length=200)

STATUS_CHOICE = (
    ('Success','Success'),
    ('Pending','Pending'),
    ('Failed','Failed'),
)


class Payment_status_ID(models.Model):
    m_tid = models.CharField(max_length=100)    
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICE)