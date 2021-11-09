from rest_framework import serializers
from .models import TradeCript, TradeCash


class CreateTradeCriptSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TradeCript
        exclude = ['create_at', 'participant', 'updated_at', 'status', 'is_active']


class RetrieveTradeCriptSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeCript
        fields = '__all__'


class RetrieveTradeCashSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeCash
        fields = '__all__'


class CreateTradeCashSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TradeCash
        exclude = ['create_at', 'participant', 'updated_at', 'status', 'is_active']


class UpdateTradeCriptSerializer(serializers.ModelSerializer):

    class Meta:

        model = TradeCript
        exclude = ['owner', 'create_at', 'participant', 'updated_at', 'status']


class UpdateTradeCashSerializer(serializers.ModelSerializer):

    class Meta:

        model = TradeCash
        exclude = ['owner', 'create_at', 'participant', 'updated_at', 'status']

