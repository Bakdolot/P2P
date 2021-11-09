from rest_framework import serializers
from .models import TradeCript, TradeCash


class CreateTradeCriptSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TradeCript
        exclude = ['create_at', 'participant', 'updated_at', 'status']


class CreateTradeCashSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TradeCash
        exclude = ['create_at', 'participant', 'updated_at', 'status']


class UpdateTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeCript
        fields = ['owner', 'is_active', 'sell_currency', 'buy_currency',
                  'sell_currency', 'buy_currency', 'sell_quantity',
                  'buy_quantity', ]


class TradeJoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeCript
        fields = ['participant']
