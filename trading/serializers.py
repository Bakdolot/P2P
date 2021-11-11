from rest_framework import serializers
from .models import Trade


class CreateTradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trade
        exclude = ['create_at', 'participant', 'updated_at', 'status', 'is_active']


class RetrieveTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'


class UpdateTradeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Trade
        fields = [
            'is_active',
            'sell_currency',
            'buy_currency',
            'sell_quantity',
            'buy_quantity',
            'description',
            'phone',
            'longitude',
            'latitude',
            'bank_card',
        ]


class AcceptCardPaymentTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ['image']


