from django_filters.rest_framework import FilterSet
from django_filters import NumericRangeFilter
from .models import Trade


class TradeListFilter(FilterSet):
    sell_quantity = NumericRangeFilter()
    buy_quantity = NumericRangeFilter()

    class Meta:
        model = Trade
        fields = [
            'sell_currency', 
            'buy_currency', 
            'buy_quantity', 
            'sell_quantity', 
            'type'
            ]
