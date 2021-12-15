from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import InternalTransfer


class CreateTransferSerializer(serializers.ModelSerializer):
    security_code = serializers.CharField(validators=[RegexValidator('^[0-9]{6,10}$', message='Пароль должен быть менее 10 символов и больше 6 символов и содержать только цифры', code='invalid_code')])
    recipient = serializers.EmailField()

    class Meta:
        model = InternalTransfer
        fields = ['id', 'owner', 'currency', 'sum', 'recipient', 'security_code', 'owner_operation']


class GetTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = InternalTransfer
        exclude = [
            'security_code',
            'owner_operation',
            'recipient_operation'
        ]


class UpdateTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = InternalTransfer
        fields= ['currency', 'sum', 'recipient', 'security_code']
