from rest_framework import serializers
from .models import *

class PaymentStatusSerializer(serializers.Serializer):
    class Meta:
        model = Payment_status_ID
        fields =["id","m_tid","payment_status"]