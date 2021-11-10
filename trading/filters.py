from django_filters.filters import RangeFilter
from django_filters.rest_framework import FilterSet
from .models import Trade


class TradeListFilter(FilterSet):
    sell_quantity = RangeFilter()
    buy_quantity = RangeFilter()

    class Meta:
        model = Trade
        fields = [
            'sell_currency', 
            'buy_currency', 
            'buy_quantity', 
            'sell_quantity', 
            'type'
            ]
