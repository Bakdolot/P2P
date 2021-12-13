from django.shortcuts import get_object_or_404

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

    def validate(self, attrs):
        get_object_or_404(Category, api_id=attrs['category_api_id'])
        get_object_or_404(Service, api_id=attrs['service_api_id'])
        return super().validate()


class PaymentRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pay24Operation
        exclude = [
            'operation_type',
            'ip_address',
        ]
