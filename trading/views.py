from decimal import Decimal
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from django.db import transaction

from .filters import TradeListFilter
from .models import EtBalance, EtCurrency, EtUsers, Trade
from .trade_services import checking_and_debiting_balance, make_transaction
from .serializers import (
    UpdateTradeSerializer, 
    CreateTradeSerializer, 
    RetrieveTradeSerializer
    )
from .permissions import IsOwnerOrReadOnly, IsOwner


class TradeListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TradeListFilter
    queryset = Trade.objects.filter(is_active=True, status='1')
    serializer_class = RetrieveTradeSerializer


class TradeCreateView(generics.CreateAPIView):
    queryset = Trade

    serializer_class = CreateTradeSerializer

    def create(self, request, *args, **kwargs):
        login = request.user.login
        data = request.POST.copy()
        if checking_and_debiting_balance(login, data['sell_quantity'], data['sell_currency']):
            data['owner'] = login
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class TradeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade
    serializer_class = UpdateTradeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveTradeSerializer
        return super().get_serializer_class()


class TradeJoinView(generics.GenericAPIView):

    def put(self, request, pk, *args, **kwargs):
        try:
            trade = generics.get_object_or_404(Trade, id=pk)
            login = request.user.login

            if trade.type == '2':
                trade.participant = login
                trade.status = '2'
                trade.save()
                return Response({'status': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)

            elif trade.type == '1':
                if checking_and_debiting_balance(login, trade.buy_quantity, trade.buy_currency):
                    trade.participant = login
                    trade.status = '2'
                    trade.save()

                    if make_transaction(trade):
                        return Response({'status': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)

            elif trade.type == '3':
                pass

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class AcceptTradeView(generics.GenericAPIView):
    permission_classes = [IsOwner]

    def put(self, request, pk, *args, **kwargs):
        try:
            with transaction.atomic():
                trade = generics.get_object_or_404(Trade.objects.filter(is_active=True, status='2', type='2'), id=pk)
                sell_currency = EtCurrency.objects.get(id=trade.sell_currency)
                user = EtBalance.objects.get(login=trade.participant, currency=sell_currency.alias)
                user.balance = str(Decimal(user.balance) + Decimal(trade.sell_quantity))
                trade.status = '3'
                trade.save()
                user.save()
                return Response({'status': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
