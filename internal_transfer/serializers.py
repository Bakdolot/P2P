from django.http import HttpResponseBadRequest
from rest_framework import serializers
from django.core.validators import RegexValidator

from .services import get_sum_with_commission, check_recipient
from .models import InternalTransfer


class CreateTransferSerializer(serializers.ModelSerializer):
    security_code = serializers.CharField(validators=[RegexValidator('\d{6,10}', message='Пароль должен быть менее 10 символов и больше 6 символов и содержать только цифры', code='invalid_code')])

    class Meta:
        model = InternalTransfer
        fields = ['owner', 'currency', 'sum', 'recipient', 'security_code', 'sum_with_commission']


class GetTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = InternalTransfer
        fields = '__all__'


class UpdateTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = InternalTransfer
        fields= ['currency', 'sum', 'recipient', 'security_code']
