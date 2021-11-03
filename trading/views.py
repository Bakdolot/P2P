from rest_framework import generics
from django_filters import rest_framework as filters

from .filters import TradeListFilter
from .models import Trade
from .serializers import UpdateTradeSerializer, CreateTradeSerializer, TradeJoinSerializer


class TradeListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TradeListFilter
    queryset = Trade.objects.filter(is_active=True)
    serializer_class = CreateTradeSerializer


class TradeCreateView(generics.CreateAPIView):
    queryset = Trade
    serializer_class = CreateTradeSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TradeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade
    serializer_class = UpdateTradeSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CreateTradeSerializer
        return super().get_serializer_class()

class TradeJoinView(generics.UpdateAPIView):
    queryset = Trade
    serializer_class = TradeJoinSerializer
