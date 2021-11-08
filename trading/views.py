from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters

from .filters import TradeListFilter
from .models import Trade, EtAuthTokens
from .trade_services import checking_and_debiting_balance
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
        data = request.POST()
        if checking_and_debiting_balance(data['token'], data['quantity'], data['currency']):
            trade = super().create(request, *args, **kwargs)
            return Response(trade, status=status.HTTP_201_CREATED)
        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class TradeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade
    serializer_class = UpdateTradeSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CreateTradeSerializer
        return super().get_serializer_class()


class TradeJoinView(generics.UpdateAPIView):
    queryset = Trade

    def update(self, request, *args, **kwargs):
        data = request.POST
        trade = generics.get_object_or_404(Trade.objects.filter(is_active=True), id=kwargs.get('pk'))
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        email = generics.get_object_or_404(EtAuthTokens, token=token)
        if checking_and_debiting_balance(data['buy_quantity'], data['buy'], email):
            trade.participant = email
            trade.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)
