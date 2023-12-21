from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from .payment import *





urlpatterns = [
    path('', index, name='home'),
    path('login/', loginphone, name='login'),
    path('payment/', phonepegateway, name='payment'),
    path('paymentgt/', PhonePayView.as_view()),
    path('paymentcheckstatus/', PhonePayCheckStatusView.as_view()),
    path('callback_url/', callback_status.as_view()),
    path("fff/",checkpaystatus,name='fff')
    # path('checkstatus/', check_status.as_view())

    # path('stataus/<str:merchantid>/<str:merchanttid>/', chchstatus.as_view())
    


]
