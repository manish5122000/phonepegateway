from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PaymentDetail)

admin.site.register(PaymentInitiate)

admin.site.register(PaymentSecret)

admin.site.register(Security)

admin.site.register(Payment_status_ID)