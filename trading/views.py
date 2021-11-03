from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Trade
from .serializers import UpdateTradeSerializer, CreateTradeSerializer, TradeJoinSerializer


class TradeListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ['sell', 'buy', 'quantity']
    queryset = Trade.objects.filter(is_active=True)
    serializer_class = CreateTradeSerializer


class TradeCreateView(generics.CreateAPIView):
    queryset = Trade
    serializer_class = CreateTradeSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TradeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return CreateTradeSerializer
        elif method == 'PUT':
            return UpdateTradeSerializer
        elif method == 'DELETE':
            return CreateTradeSerializer


class TradeJoinView(generics.UpdateAPIView):
    queryset = Trade
    serializer_class = TradeJoinSerializer
