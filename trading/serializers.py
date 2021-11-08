from rest_framework import serializers
from .models import Trade


class CreateTradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trade
        exclude = ['create_at', 'owner']


class UpdateTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ['owner', 'is_active', 'sell_currency', 'buy_currency',
                  'sell_currency', 'buy_currency', 'sell_quantity',
                  'buy_quantity', 'type']


class TradeJoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ['participant']
