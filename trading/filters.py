from django_filters.rest_framework import FilterSet
from django_filters import NumericRangeFilter
from .models import Trade


class TradeListFilter(FilterSet):
    quantity = NumericRangeFilter()

    class Meta:
        model = Trade
        fields = ['sell_currency', 'buy_currency', 'quantity']
