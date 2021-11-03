from rest_framework import serializers
from .models import Trade


class CreateTradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trade
        exclude = ['create_at']


class UpdateTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ['owner', 'is_active', 'sell', 'buy', 'quantity', 'type']


class TradeJoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ['participant']
