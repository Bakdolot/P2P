from django_filters.rest_framework import FilterSet
from django_filters import NumericRangeFilter
from .models import TradeCash, TradeCript


class TradeListFilter(FilterSet):
    quantity = NumericRangeFilter()

    class Meta:
        model = TradeCript
        fields = ['sell_currency', 'buy_currency', 'quantity']
