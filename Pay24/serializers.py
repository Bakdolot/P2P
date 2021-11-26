from rest_framework import serializers
from .models import *


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ServiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class CreatePaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pay24Operation
        fields = [
            'category',
            'service',
            'sum',
        ]


class PaymentRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pay24Operation
        exclude = [
            'operation_type',
            'ip_address',
        ]
