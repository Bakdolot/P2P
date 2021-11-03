from rest_framework import generics, serializers
from django_filters import rest_framework as filters
from .models import Trade
from .serializers import TradeSerializer, CreateTradeSerializer


class TradeListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ['sell', 'buy', 'quantity']
    queryset = Trade.objects.filter(is_active=True)
    serializer_class = TradeSerializer


class TradeCreateView(generics.CreateAPIView):
    queryset = Trade
    serializer_class = CreateTradeSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TradeUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade
    serializer_class = TradeSerializer
