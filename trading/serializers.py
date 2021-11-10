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
        exclude = ['owner', 'create_at', 'participant', 'updated_at', 'status']
