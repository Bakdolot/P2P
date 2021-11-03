from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trade
        exclude = ['create_at']


class CreateTradeSerializer(serializers.Serializer):
    TYPE_CHOICES = (
        ('1', 'Крипта'),
        ('2', 'Карта'),
        ('3', 'Наличка')
    )

    owner = serializers.CharField(max_length=150)
    sell = serializers.IntegerField()
    buy = serializers.IntegerField()
    quantity = serializers.DecimalField(max_digits=19, decimal_places=2)
    type = serializers.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        fields = ('owner', 'sell', 'buy', 'quantity', 'type')
