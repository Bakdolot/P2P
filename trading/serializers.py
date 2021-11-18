from rest_framework import serializers
from .models import Trade


class CreateTradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trade

        exclude = [
            'create_at', 
            'participant', 
            'updated_at', 
            'status', 
            'owner_confirm',
            'participant_sent',
            'sell_quantity_with_commission',
            'participant_operation'
            ]


class RetrieveTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'


class UpdateTradeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Trade
        fields = [
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
